#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

OUT_DIR = "/tmp/codex-android"
PKG = "com.fender.tone"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(SKILL_DIR, ".env")


def run(args, check=True, capture=True):
    kwargs = {"text": True}
    if capture:
        kwargs.update({"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT})
    proc = subprocess.run(args, **kwargs)
    if check and proc.returncode != 0:
        if capture and proc.stdout:
            print(proc.stdout, end="")
        raise SystemExit(proc.returncode)
    return proc.stdout if capture else ""


def adb(*args, check=True, capture=True):
    return run(["adb", *args], check=check, capture=capture)


def load_env():
    values = {}
    if not os.path.exists(ENV_FILE):
        return values
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("'\"")
    return values


def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)


def status(_args):
    print(adb("devices", "-l"), end="")
    for prop in ("ro.product.model", "ro.build.version.release"):
        print(f"{prop}: {adb('shell', 'getprop', prop).strip()}")
    print(adb("shell", "wm", "size").strip())
    window = adb("shell", "dumpsys", "window")
    for line in window.splitlines():
        if "mCurrentFocus" in line or "mFocusedApp" in line:
            print(line.strip())


def launch(_args):
    adb("shell", "monkey", "-p", PKG, "-c", "android.intent.category.LAUNCHER", "1")


def snapshot(args):
    ensure_out_dir()
    prefix = args.prefix or "fender-tone"
    png, xml = capture_snapshot(prefix)
    print(png)
    print(xml)


def capture_snapshot(prefix):
    ensure_out_dir()
    png = os.path.join(OUT_DIR, f"{prefix}.png")
    xml = os.path.join(OUT_DIR, f"{prefix}.xml")
    with open(png, "wb") as f:
        proc = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)
    adb("shell", "uiautomator", "dump", "/sdcard/window.xml")
    adb("pull", "/sdcard/window.xml", xml)
    return png, xml


def ui_text(args):
    xml = args.xml or os.path.join(OUT_DIR, "fender-tone.xml")
    if not os.path.exists(xml):
        class O:
            prefix = "fender-tone"
        snapshot(O())
    root = ET.parse(xml).getroot()
    for node in root.iter("node"):
        text = node.attrib.get("text", "")
        desc = node.attrib.get("content-desc", "")
        rid = node.attrib.get("resource-id", "")
        cls = node.attrib.get("class", "")
        bounds = node.attrib.get("bounds", "")
        if text or desc or PKG in rid:
            print(f"text={text!r} desc={desc!r} id={rid!r} class={cls!r} bounds={bounds}")


def tap(args):
    adb("shell", "input", "tap", str(args.x), str(args.y))


def key(args):
    adb("shell", "input", "keyevent", args.key)


def unlock(_args):
    pin = load_env().get("ANDROID_PIN")
    if not pin:
        raise SystemExit(f"ANDROID_PIN is not set in {ENV_FILE}")
    adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")
    adb("shell", "input", "swipe", "360", "1250", "360", "300", "500")
    adb("shell", "input", "text", pin)
    adb("shell", "input", "keyevent", "KEYCODE_ENTER")


def stay_awake(_args):
    adb("shell", "svc", "power", "stayon", "usb")


def audit_snapshot(args):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_label = "".join(c if c.isalnum() or c in "-_" else "-" for c in args.label).strip("-")
    prefix = f"audit-{stamp}-{safe_label or 'state'}"
    png, xml = capture_snapshot(prefix)
    meta = os.path.join(OUT_DIR, f"{prefix}.txt")
    lines = [
        f"label: {args.label}",
        f"timestamp: {stamp}",
        "adb devices:",
        adb("devices", "-l").rstrip(),
        "",
        "device:",
        f"model: {adb('shell', 'getprop', 'ro.product.model').strip()}",
        f"android: {adb('shell', 'getprop', 'ro.build.version.release').strip()}",
        adb("shell", "wm", "size").strip(),
        "",
        "window:",
    ]
    window = adb("shell", "dumpsys", "window")
    lines.extend(line.strip() for line in window.splitlines() if "mCurrentFocus" in line or "mFocusedApp" in line)
    with open(meta, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(png)
    print(xml)
    print(meta)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("status")
    p.set_defaults(func=status)

    p = sub.add_parser("launch")
    p.set_defaults(func=launch)

    p = sub.add_parser("snapshot")
    p.add_argument("--prefix")
    p.set_defaults(func=snapshot)

    p = sub.add_parser("ui-text")
    p.add_argument("--xml")
    p.set_defaults(func=ui_text)

    p = sub.add_parser("tap")
    p.add_argument("x", type=int)
    p.add_argument("y", type=int)
    p.set_defaults(func=tap)

    p = sub.add_parser("key")
    p.add_argument("key")
    p.set_defaults(func=key)

    p = sub.add_parser("unlock")
    p.set_defaults(func=unlock)

    p = sub.add_parser("stay-awake")
    p.set_defaults(func=stay_awake)

    p = sub.add_parser("audit-snapshot")
    p.add_argument("--label", default="state")
    p.set_defaults(func=audit_snapshot)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
