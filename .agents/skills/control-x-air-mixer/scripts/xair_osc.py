#!/usr/bin/env python3
"""Minimal, safety-oriented OSC client for Behringer X AIR mixers."""

from __future__ import annotations

import argparse
import json
import os
import socket
import struct
import sys
import time
from dataclasses import dataclass
from typing import Any, Iterable


DEFAULT_HOST = os.environ.get("XAIR_HOST", "192.168.1.149")
DEFAULT_PORT = 10024
DEFAULT_TIMEOUT = 0.8
MAX_LABEL_LENGTH = 12
COLOR_VALUES = {
    "off": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7,
}


class XAirError(RuntimeError):
    pass


def _pad4(data: bytes) -> bytes:
    return data + (b"\0" * ((-len(data)) % 4))


def _osc_string(value: str) -> bytes:
    if "\0" in value:
        raise XAirError("OSC strings cannot contain NUL bytes")
    return _pad4(value.encode("utf-8") + b"\0")


def encode_message(address: str, values: Iterable[Any] = ()) -> bytes:
    if not address.startswith("/"):
        raise XAirError(f"OSC address must start with '/': {address!r}")

    tags = [","]
    payload: list[bytes] = []
    for value in values:
        if isinstance(value, bool):
            tags.append("i")
            payload.append(struct.pack(">i", int(value)))
        elif isinstance(value, int):
            tags.append("i")
            payload.append(struct.pack(">i", value))
        elif isinstance(value, float):
            tags.append("f")
            payload.append(struct.pack(">f", value))
        elif isinstance(value, str):
            tags.append("s")
            payload.append(_osc_string(value))
        elif isinstance(value, bytes):
            tags.append("b")
            payload.append(struct.pack(">i", len(value)) + _pad4(value))
        else:
            raise XAirError(f"unsupported OSC value type: {type(value).__name__}")

    return _osc_string(address) + _osc_string("".join(tags)) + b"".join(payload)


def _read_string(data: bytes, offset: int) -> tuple[str, int]:
    end = data.find(b"\0", offset)
    if end < 0:
        raise XAirError("unterminated OSC string")
    try:
        value = data[offset:end].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise XAirError("invalid UTF-8 in OSC string") from exc
    return value, (end + 4) & ~3


def decode_message(data: bytes) -> tuple[str, list[Any]]:
    address, offset = _read_string(data, 0)
    if address == "#bundle":
        raise XAirError("OSC bundles are not supported by this initial client")
    tags, offset = _read_string(data, offset)
    if not tags.startswith(","):
        raise XAirError("missing OSC type tag string")

    values: list[Any] = []
    for tag in tags[1:]:
        if tag == "i":
            if offset + 4 > len(data):
                raise XAirError("truncated OSC integer")
            values.append(struct.unpack_from(">i", data, offset)[0])
            offset += 4
        elif tag == "f":
            if offset + 4 > len(data):
                raise XAirError("truncated OSC float")
            values.append(struct.unpack_from(">f", data, offset)[0])
            offset += 4
        elif tag == "s":
            value, offset = _read_string(data, offset)
            values.append(value)
        elif tag == "b":
            if offset + 4 > len(data):
                raise XAirError("truncated OSC blob length")
            size = struct.unpack_from(">i", data, offset)[0]
            offset += 4
            if size < 0 or offset + size > len(data):
                raise XAirError("invalid OSC blob length")
            values.append(data[offset : offset + size])
            offset += (size + 3) & ~3
        else:
            raise XAirError(f"unsupported OSC type tag: {tag!r}")
    return address, values


@dataclass
class XAirClient:
    host: str
    port: int = DEFAULT_PORT
    timeout: float = DEFAULT_TIMEOUT

    def __post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 0))
        self.sock.settimeout(self.timeout)

    def close(self) -> None:
        self.sock.close()

    def __enter__(self) -> "XAirClient":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _tb: Any) -> None:
        self.close()

    def send(self, address: str, *values: Any) -> None:
        self.sock.sendto(encode_message(address, values), (self.host, self.port))

    def request(self, address: str) -> list[Any]:
        self.send(address)
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise XAirError(
                    f"no response for {address} from {self.host}:{self.port}"
                )
            self.sock.settimeout(remaining)
            try:
                packet, peer = self.sock.recvfrom(65535)
            except socket.timeout as exc:
                raise XAirError(
                    f"no response for {address} from {self.host}:{self.port}"
                ) from exc
            if peer[0] != socket.gethostbyname(self.host):
                continue
            response_address, values = decode_message(packet)
            if response_address == address:
                return values


def _json_value(value: Any) -> Any:
    if isinstance(value, bytes):
        return {"blob_hex": value.hex(), "length": len(value)}
    return value


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def require_single_value(values: list[Any], path: str) -> Any:
    if len(values) != 1:
        raise XAirError(f"expected one value for {path}, received {len(values)}")
    return values[0]


def validate_label(label: str) -> None:
    if not label.strip():
        raise XAirError("label cannot be blank")
    if len(label) > MAX_LABEL_LENGTH:
        raise XAirError(
            f"label is {len(label)} characters; X AIR labels allow at most "
            f"{MAX_LABEL_LENGTH}"
        )
    if "\0" in label:
        raise XAirError("label cannot contain NUL bytes")


def label_path(kind: str, number: int) -> str:
    if kind == "channel":
        if not 1 <= number <= 16:
            raise XAirError("channel number must be between 1 and 16")
        return f"/ch/{number:02d}/config/name"
    if kind == "bus":
        if not 1 <= number <= 6:
            raise XAirError("bus number must be between 1 and 6")
        return f"/bus/{number}/config/name"
    raise XAirError(f"unsupported label target: {kind}")


def color_path(kind: str, number: int) -> str:
    if kind == "channel":
        if not 1 <= number <= 16:
            raise XAirError("channel number must be between 1 and 16")
        return f"/ch/{number:02d}/config/color"
    if kind == "bus":
        if not 1 <= number <= 6:
            raise XAirError("bus number must be between 1 and 6")
        return f"/bus/{number}/config/color"
    raise XAirError(f"unsupported color target: {kind}")


def command_self_test(_args: argparse.Namespace) -> None:
    cases = [
        ("/xinfo", [], encode_message("/xinfo")),
        ("/ch/01/config/name", ["Bass"], encode_message("/ch/01/config/name", ["Bass"])),
        ("/test", [7, 0.5, True], encode_message("/test", [7, 0.5, True])),
        ("/blob", [b"abc"], encode_message("/blob", [b"abc"])),
    ]
    for expected_address, expected_values, packet in cases:
        address, values = decode_message(packet)
        if address != expected_address or values != expected_values:
            raise XAirError(
                f"self-test failed: {(address, values)!r} != "
                f"{(expected_address, expected_values)!r}"
            )
    if color_path("channel", 16) != "/ch/16/config/color":
        raise XAirError("self-test failed: channel color path")
    if color_path("bus", 6) != "/bus/6/config/color":
        raise XAirError("self-test failed: bus color path")
    if COLOR_VALUES != {
        "off": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
    }:
        raise XAirError("self-test failed: color mapping")
    emit({"ok": True, "tests": len(cases) + 3})


def command_probe(args: argparse.Namespace) -> None:
    with XAirClient(args.host, args.port, args.timeout) as client:
        values = client.request("/xinfo")
    fields = ["ip", "name", "model", "firmware"]
    info = {key: values[index] for index, key in enumerate(fields) if index < len(values)}
    emit(
        {
            "host": args.host,
            "operation": "probe",
            "port": args.port,
            "response": info,
            "values": [_json_value(value) for value in values],
        }
    )


def command_get(args: argparse.Namespace) -> None:
    with XAirClient(args.host, args.port, args.timeout) as client:
        values = client.request(args.path)
    emit(
        {
            "host": args.host,
            "operation": "get",
            "path": args.path,
            "port": args.port,
            "values": [_json_value(value) for value in values],
        }
    )


def command_label(args: argparse.Namespace) -> None:
    validate_label(args.label)
    path = label_path(args.label_kind, args.number)
    with XAirClient(args.host, args.port, args.timeout) as client:
        before = require_single_value(client.request(path), path)
        result: dict[str, Any] = {
            "applied": False,
            "before": _json_value(before),
            "host": args.host,
            "operation": f"label-{args.label_kind}",
            "path": path,
            "port": args.port,
            "requested": args.label,
        }
        if not args.apply or before == args.label:
            result["verified"] = _json_value(before)
            emit(result)
            return

        client.send(path, args.label)
        verified = None
        for _attempt in range(3):
            try:
                verified = require_single_value(client.request(path), path)
            except XAirError:
                continue
            if verified == args.label:
                break
        if verified != args.label:
            raise XAirError(
                f"write verification failed for {path}: expected {args.label!r}, "
                f"received {verified!r}"
            )
        result["applied"] = True
        result["verified"] = _json_value(verified)
        emit(result)


def command_color(args: argparse.Namespace) -> None:
    path = color_path(args.color_kind, args.number)
    requested = COLOR_VALUES[args.color]
    with XAirClient(args.host, args.port, args.timeout) as client:
        before = require_single_value(client.request(path), path)
        if not isinstance(before, int):
            raise XAirError(
                f"expected integer color value for {path}, received {before!r}"
            )
        result: dict[str, Any] = {
            "applied": False,
            "before": before,
            "before_name": next(
                (name for name, value in COLOR_VALUES.items() if value == before),
                None,
            ),
            "host": args.host,
            "operation": f"color-{args.color_kind}",
            "path": path,
            "port": args.port,
            "requested": requested,
            "requested_name": args.color,
        }
        if not args.apply or before == requested:
            result["verified"] = before
            result["verified_name"] = result["before_name"]
            emit(result)
            return

        client.send(path, requested)
        verified = None
        for _attempt in range(3):
            try:
                verified = require_single_value(client.request(path), path)
            except XAirError:
                continue
            if verified == requested:
                break
        if verified != requested:
            raise XAirError(
                f"write verification failed for {path}: expected {requested!r}, "
                f"received {verified!r}"
            )
        result["applied"] = True
        result["verified"] = verified
        result["verified_name"] = args.color
        emit(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safely inspect and identify a Behringer X AIR mixer over OSC"
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"mixer IP/host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    commands = parser.add_subparsers(dest="command", required=True)

    command = commands.add_parser("self-test", help="test OSC encoding/decoding locally")
    command.set_defaults(func=command_self_test)

    command = commands.add_parser("probe", help="read mixer identity with /xinfo")
    command.set_defaults(func=command_probe)

    command = commands.add_parser("get", help="read one OSC parameter")
    command.add_argument("path")
    command.set_defaults(func=command_get)

    for kind, limit in (("channel", "1-16"), ("bus", "1-6")):
        command = commands.add_parser(
            f"label-{kind}", help=f"preview or apply a {kind} label"
        )
        command.add_argument("number", type=int, help=f"{kind} number ({limit})")
        command.add_argument("label", help=f"label, up to {MAX_LABEL_LENGTH} characters")
        command.add_argument(
            "--apply",
            action="store_true",
            help="write and verify; without this flag the command is read-only",
        )
        command.set_defaults(func=command_label, label_kind=kind)

        command = commands.add_parser(
            f"color-{kind}", help=f"preview or apply a {kind} scribble-strip color"
        )
        command.add_argument("number", type=int, help=f"{kind} number ({limit})")
        command.add_argument(
            "color",
            choices=tuple(COLOR_VALUES),
            help="scribble-strip color",
        )
        command.add_argument(
            "--apply",
            action="store_true",
            help="write and verify; without this flag the command is read-only",
        )
        command.set_defaults(func=command_color, color_kind=kind)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.func(args)
        return 0
    except (OSError, XAirError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
