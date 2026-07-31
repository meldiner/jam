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
FADER_POSITIONS = {
    "minimum": 0.0,
    "unity": 0.75,
}
HEADAMP_GAIN_MIN_DB = -12.0
HEADAMP_GAIN_MAX_DB = 60.0
HEADAMP_GAIN_STEP_DB = 0.5
# XR18V2 stores normalized controls on a 10-bit-style grid. For example,
# requested unity 0.75 reads back as 0.7497556209564209. Half of one 1/1023
# step is about 0.000489, so 0.0005 accepts hardware quantization without
# accepting a neighboring control step.
FLOAT_VERIFY_TOLERANCE = 0.0005


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


def fader_path(kind: str, number: int | None = None) -> str:
    if kind == "channel":
        if number is None or not 1 <= number <= 16:
            raise XAirError("channel number must be between 1 and 16")
        return f"/ch/{number:02d}/mix/fader"
    if kind == "bus":
        if number is None or not 1 <= number <= 6:
            raise XAirError("bus number must be between 1 and 6")
        return f"/bus/{number}/mix/fader"
    if kind == "main":
        if number is not None:
            raise XAirError("main fader does not accept a number")
        return "/lr/mix/fader"
    raise XAirError(f"unsupported fader target: {kind}")


def channel_bus_send_path(channel: int, bus: int) -> str:
    if not 1 <= channel <= 16:
        raise XAirError("channel number must be between 1 and 16")
    if not 1 <= bus <= 6:
        raise XAirError("bus number must be between 1 and 6")
    return f"/ch/{channel:02d}/mix/{bus:02d}/level"


def validate_return_target(target: str) -> None:
    if target != "aux" and target not in {"1", "2", "3", "4"}:
        raise XAirError("return target must be aux or an FX return from 1 to 4")


def return_fader_path(target: str) -> str:
    validate_return_target(target)
    return f"/rtn/{target}/mix/fader"


def return_bus_send_path(target: str, bus: int) -> str:
    validate_return_target(target)
    if not 1 <= bus <= 6:
        raise XAirError("bus number must be between 1 and 6")
    return f"/rtn/{target}/mix/{bus:02d}/level"


def headamp_gain_path(number: int) -> str:
    if not 1 <= number <= 16:
        raise XAirError("headamp number must be between 1 and 16")
    return f"/headamp/{number:02d}/gain"


def validate_headamp_gain_db(gain_db: float) -> None:
    if not HEADAMP_GAIN_MIN_DB <= gain_db <= HEADAMP_GAIN_MAX_DB:
        raise XAirError(
            f"headamp gain must be between {HEADAMP_GAIN_MIN_DB:g} and "
            f"{HEADAMP_GAIN_MAX_DB:g} dB"
        )
    steps = (gain_db - HEADAMP_GAIN_MIN_DB) / HEADAMP_GAIN_STEP_DB
    if abs(steps - round(steps)) > 1e-9:
        raise XAirError(
            f"headamp gain must use {HEADAMP_GAIN_STEP_DB:g} dB steps"
        )


def headamp_db_to_normalized(gain_db: float) -> float:
    validate_headamp_gain_db(gain_db)
    return (gain_db - HEADAMP_GAIN_MIN_DB) / (
        HEADAMP_GAIN_MAX_DB - HEADAMP_GAIN_MIN_DB
    )


def headamp_normalized_to_db(value: float) -> float:
    return HEADAMP_GAIN_MIN_DB + value * (
        HEADAMP_GAIN_MAX_DB - HEADAMP_GAIN_MIN_DB
    )


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
    if fader_path("channel", 16) != "/ch/16/mix/fader":
        raise XAirError("self-test failed: channel fader path")
    if fader_path("bus", 6) != "/bus/6/mix/fader":
        raise XAirError("self-test failed: bus fader path")
    if fader_path("main") != "/lr/mix/fader":
        raise XAirError("self-test failed: main fader path")
    if headamp_gain_path(1) != "/headamp/01/gain":
        raise XAirError("self-test failed: headamp path")
    if channel_bus_send_path(16, 6) != "/ch/16/mix/06/level":
        raise XAirError("self-test failed: channel bus-send path")
    if return_fader_path("aux") != "/rtn/aux/mix/fader":
        raise XAirError("self-test failed: Aux return fader path")
    if return_bus_send_path("4", 6) != "/rtn/4/mix/06/level":
        raise XAirError("self-test failed: FX return bus-send path")
    if abs(headamp_db_to_normalized(0.0) - (1.0 / 6.0)) > 1e-9:
        raise XAirError("self-test failed: 0 dB headamp conversion")
    if abs(headamp_normalized_to_db(0.375) - 15.0) > 1e-9:
        raise XAirError("self-test failed: normalized headamp conversion")
    emit({"ok": True, "tests": len(cases) + 12})


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


def command_fader(args: argparse.Namespace) -> None:
    if args.fader_kind == "channel-send":
        path = channel_bus_send_path(args.channel, args.bus)
    elif args.fader_kind == "return":
        path = return_fader_path(args.target)
    elif args.fader_kind == "return-send":
        path = return_bus_send_path(args.target, args.bus)
    else:
        number = getattr(args, "number", None)
        path = fader_path(args.fader_kind, number)
    requested = FADER_POSITIONS[args.position]
    with XAirClient(args.host, args.port, args.timeout) as client:
        before = require_single_value(client.request(path), path)
        if not isinstance(before, float):
            raise XAirError(
                f"expected float fader value for {path}, received {before!r}"
            )
        result: dict[str, Any] = {
            "applied": False,
            "before_normalized": before,
            "host": args.host,
            "operation": f"set-{args.fader_kind}-fader",
            "path": path,
            "port": args.port,
            "requested_normalized": requested,
            "requested_position": args.position,
            "requested_db": "-inf" if args.position == "minimum" else 0.0,
        }
        if not args.apply or abs(before - requested) <= FLOAT_VERIFY_TOLERANCE:
            result["verified_normalized"] = before
            emit(result)
            return

        client.send(path, requested)
        verified = None
        for _attempt in range(3):
            try:
                candidate = require_single_value(client.request(path), path)
            except XAirError:
                continue
            if isinstance(candidate, float):
                verified = candidate
            if verified is not None and abs(verified - requested) <= FLOAT_VERIFY_TOLERANCE:
                break
        if verified is None or abs(verified - requested) > FLOAT_VERIFY_TOLERANCE:
            raise XAirError(
                f"write verification failed for {path}: expected {requested!r}, "
                f"received {verified!r}"
            )
        result["applied"] = True
        result["verified_normalized"] = verified
        emit(result)


def command_headamp_gain(args: argparse.Namespace) -> None:
    validate_headamp_gain_db(args.gain_db)
    path = headamp_gain_path(args.number)
    requested = headamp_db_to_normalized(args.gain_db)
    with XAirClient(args.host, args.port, args.timeout) as client:
        before = require_single_value(client.request(path), path)
        if not isinstance(before, float):
            raise XAirError(
                f"expected float headamp value for {path}, received {before!r}"
            )
        result: dict[str, Any] = {
            "applied": False,
            "before_db": headamp_normalized_to_db(before),
            "before_normalized": before,
            "host": args.host,
            "operation": "set-headamp-gain",
            "path": path,
            "port": args.port,
            "requested_db": args.gain_db,
            "requested_normalized": requested,
        }
        if not args.apply or abs(before - requested) <= FLOAT_VERIFY_TOLERANCE:
            result["verified_db"] = headamp_normalized_to_db(before)
            result["verified_normalized"] = before
            emit(result)
            return

        client.send(path, requested)
        verified = None
        for _attempt in range(3):
            try:
                candidate = require_single_value(client.request(path), path)
            except XAirError:
                continue
            if isinstance(candidate, float):
                verified = candidate
            if verified is not None and abs(verified - requested) <= FLOAT_VERIFY_TOLERANCE:
                break
        if verified is None or abs(verified - requested) > FLOAT_VERIFY_TOLERANCE:
            raise XAirError(
                f"write verification failed for {path}: expected {requested!r}, "
                f"received {verified!r}"
            )
        result["applied"] = True
        result["verified_db"] = headamp_normalized_to_db(verified)
        result["verified_normalized"] = verified
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

        command = commands.add_parser(
            f"set-{kind}-fader",
            help=f"preview or set a {kind} fader to unity or minimum",
        )
        command.add_argument("number", type=int, help=f"{kind} number ({limit})")
        command.add_argument("position", choices=tuple(FADER_POSITIONS))
        command.add_argument(
            "--apply",
            action="store_true",
            help="write and verify; without this flag the command is read-only",
        )
        command.set_defaults(func=command_fader, fader_kind=kind)

    command = commands.add_parser(
        "set-main-fader", help="preview or set the Main LR fader to unity or minimum"
    )
    command.add_argument("position", choices=tuple(FADER_POSITIONS))
    command.add_argument(
        "--apply",
        action="store_true",
        help="write and verify; without this flag the command is read-only",
    )
    command.set_defaults(func=command_fader, fader_kind="main")

    command = commands.add_parser(
        "set-channel-bus-send",
        help="preview or set one channel's send level to one bus",
    )
    command.add_argument("channel", type=int, help="input channel number (1-16)")
    command.add_argument("bus", type=int, help="bus number (1-6)")
    command.add_argument("position", choices=tuple(FADER_POSITIONS))
    command.add_argument(
        "--apply",
        action="store_true",
        help="write and verify; without this flag the command is read-only",
    )
    command.set_defaults(func=command_fader, fader_kind="channel-send")

    command = commands.add_parser(
        "set-return-fader",
        help="preview or set the Aux input or an FX return's Main fader",
    )
    command.add_argument("target", choices=("aux", "1", "2", "3", "4"))
    command.add_argument("position", choices=tuple(FADER_POSITIONS))
    command.add_argument(
        "--apply",
        action="store_true",
        help="write and verify; without this flag the command is read-only",
    )
    command.set_defaults(func=command_fader, fader_kind="return")

    command = commands.add_parser(
        "set-return-bus-send",
        help="preview or set the Aux input or an FX return's send to one bus",
    )
    command.add_argument("target", choices=("aux", "1", "2", "3", "4"))
    command.add_argument("bus", type=int, help="bus number (1-6)")
    command.add_argument("position", choices=tuple(FADER_POSITIONS))
    command.add_argument(
        "--apply",
        action="store_true",
        help="write and verify; without this flag the command is read-only",
    )
    command.set_defaults(func=command_fader, fader_kind="return-send")

    command = commands.add_parser(
        "set-headamp-gain", help="preview or set one analog input preamp gain"
    )
    command.add_argument("number", type=int, help="headamp/input number (1-16)")
    command.add_argument("gain_db", type=float, help="gain in dB (-12 to +60, 0.5 dB steps)")
    command.add_argument(
        "--apply",
        action="store_true",
        help="write and verify; without this flag the command is read-only",
    )
    command.set_defaults(func=command_headamp_gain)

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
