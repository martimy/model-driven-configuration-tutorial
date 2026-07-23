#!/usr/bin/env python3

import argparse
import csv
import html
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from pygnmi.client import gNMIclient


DEVICES = {
    "srl-01": {
        "target": ("srl-01", 57400),
        "username": "admin",
        "password": "NokiaSrl1!",
        "skip_verify": True,
    },
    "srl-02": {
        "target": ("srl-02", 57400),
        "username": "admin",
        "password": "NokiaSrl1!",
        "skip_verify": True,
    },
}

CPU_PATH = "/platform/control[slot=A]/cpu[index=all]/total"


def suppress_expected_grpc_cancel(args):
    if "Channel closed" in str(args.exc_value):
        return
    sys.__excepthook__(args.exc_type, args.exc_value, args.exc_traceback)


threading.excepthook = suppress_expected_grpc_cancel


def docker_cmd(container, command):
    base = ["docker", "exec", container, "sh", "-lc", command]
    if os.geteuid() != 0:
        probe = subprocess.run(
            ["docker", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if probe.returncode != 0:
            base = ["sg", "docker", "-c", " ".join(shell_quote(part) for part in base)]
    return base


def shell_quote(value):
    return "'" + value.replace("'", "'\"'\"'") + "'"


def start_cpu_load(container, workers):
    if workers <= 0:
        return None

    load_script = (
        "trap 'kill 0' TERM INT; "
        "for i in $(seq 1 %d); do "
        "(while :; do :; done) >/dev/null 2>&1 & "
        "done; "
        "wait"
    ) % workers

    # Keep the workers in one process group so cleanup can kill them reliably.
    command = "setsid sh -lc %s >/dev/null 2>&1 & echo $!" % shell_quote(load_script)
    proc = subprocess.run(
        docker_cmd(container, command),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    pid = proc.stdout.strip().splitlines()[-1]
    return pid


def stop_cpu_load(container, pid):
    if not pid:
        return
    command = "kill -- -%s 2>/dev/null || kill %s 2>/dev/null || true" % (pid, pid)
    subprocess.run(
        docker_cmd(container, command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def extract_value(message):
    for update in message.get("update", {}).get("update", []):
        value = update.get("val")
        if isinstance(value, dict) and "instant" in value:
            return value["instant"]
        if isinstance(value, (int, float)):
            return value
    return None


def collect_samples(device, duration, interval):
    subscribe = {
        "subscription": [
            {
                "path": CPU_PATH,
                "mode": "sample",
                "sample_interval": int(interval * 1_000_000_000),
            }
        ],
        "mode": "stream",
        "encoding": "json_ietf",
    }

    samples = []
    started = time.monotonic()
    with gNMIclient(**DEVICES[device]) as client:
        stream = client.subscribe2(subscribe=subscribe)
        try:
            while True:
                message = stream.get_update(timeout=max(5, interval * 2))
                value = extract_value(message)
                elapsed = time.monotonic() - started
                if isinstance(value, (int, float)):
                    samples.append((elapsed, float(value)))
                    print(f"{elapsed:6.1f}s  cpu={value:5.1f}%")
                if elapsed >= duration:
                    break
        finally:
            stream.close()
    return samples


def write_csv(path, samples):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seconds", "cpu_percent"])
        writer.writerows((round(t, 3), round(v, 3)) for t, v in samples)


def write_svg(path, samples, title):
    width, height = 960, 420
    left, right, top, bottom = 58, 24, 38, 48
    chart_w = width - left - right
    chart_h = height - top - bottom
    max_t = max((t for t, _ in samples), default=1)

    def x_for(t):
        return left + (t / max_t) * chart_w

    def y_for(v):
        return top + chart_h - (max(0, min(100, v)) / 100) * chart_h

    points = " ".join(f"{x_for(t):.1f},{y_for(v):.1f}" for t, v in samples)
    circles = "\n".join(
        f'<circle cx="{x_for(t):.1f}" cy="{y_for(v):.1f}" r="3" />'
        for t, v in samples
    )
    grid = []
    for pct in range(0, 101, 20):
        y = y_for(pct)
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid" />'
        )
        grid.append(f'<text x="12" y="{y+4:.1f}" class="tick">{pct}%</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    text {{ font-family: Arial, sans-serif; fill: #202124; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 13px; }}
    .tick {{ font-size: 12px; fill: #5f6368; }}
    .grid {{ stroke: #d6d9de; stroke-width: 1; }}
    .axis {{ stroke: #202124; stroke-width: 1.5; }}
    polyline {{ fill: none; stroke: #0b7285; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }}
    circle {{ fill: #0b7285; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{left}" y="25" class="title">{html.escape(title)}</text>
  {''.join(grid)}
  <line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" class="axis" />
  <line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" class="axis" />
  <polyline points="{points}" />
  {circles}
  <text x="{width/2:.0f}" y="{height-12}" class="label" text-anchor="middle">seconds</text>
  <text x="18" y="{height/2:.0f}" class="label" transform="rotate(-90 18 {height/2:.0f})" text-anchor="middle">CPU utilization</text>
</svg>
'''
    path.write_text(svg)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Increase SR Linux CPU load, subscribe to CPU telemetry over gNMI, and plot it."
    )
    parser.add_argument("device", choices=sorted(DEVICES), nargs="?", default="srl-01")
    parser.add_argument("--duration", type=float, default=60.0, help="seconds to collect")
    parser.add_argument("--interval", type=float, default=2.0, help="sample interval in seconds")
    parser.add_argument("--workers", type=int, default=2, help="CPU load workers inside the container")
    parser.add_argument("--out-dir", default="artifacts", help="directory for csv/svg output")
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    csv_path = out_dir / f"{args.device}-cpu-{stamp}.csv"
    svg_path = out_dir / f"{args.device}-cpu-{stamp}.svg"

    pid = None
    try:
        pid = start_cpu_load(args.device, args.workers)
        if pid:
            print(f"Started CPU load in {args.device}, process group {pid}")
        samples = collect_samples(args.device, args.duration, args.interval)
    finally:
        stop_cpu_load(args.device, pid)
        if pid:
            print(f"Stopped CPU load in {args.device}")

    if not samples:
        print("No CPU samples received from gNMI.", file=sys.stderr)
        return 1

    write_csv(csv_path, samples)
    write_svg(svg_path, samples, f"{args.device} CPU via gNMI subscription")
    print(f"Wrote {csv_path}")
    print(f"Wrote {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
