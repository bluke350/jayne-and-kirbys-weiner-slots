#!/usr/bin/env python3
"""Jayne & Kirby's Weiner Slots - tiny static server with phone-friendly LAN mode.

Run with:  python3 app.py
Then open: http://localhost:8000
If 8000 is busy:  PORT=8080 python3 app.py
Bind to one interface only:  HOST=127.0.0.1 python3 app.py
"""

from __future__ import annotations

import functools
import os
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_port() -> int:
    """Allow PORT=8080 python3 app.py when 8000 is busy."""
    raw = os.environ.get("PORT", str(PORT))
    try:
        port = int(raw)
    except ValueError:
        print(f"PORT must be a number, got {raw!r}.")
        raise SystemExit(2)
    if not 1 <= port <= 65535:
        print(f"PORT must be between 1 and 65535, got {port}.")
        raise SystemExit(2)
    return port


def lan_address() -> str:
    """Best-effort LAN IP so a phone on the same Wi-Fi can connect."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "127.0.0.1"
    finally:
        probe.close()


class SlotHandler(SimpleHTTPRequestHandler):
    """Static handler with no-cache headers so edits show up instantly."""

    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
    }

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stdout.write("[weiner-slots] " + (fmt % args) + "\n")


def main() -> int:
    port = resolve_port()
    host = os.environ.get("HOST", HOST)
    handler = functools.partial(SlotHandler, directory=BASE_DIR)
    ThreadingHTTPServer.allow_reuse_address = True

    try:
        httpd = ThreadingHTTPServer((host, port), handler)
    except OSError as exc:
        if exc.errno in (48, 98):
            print(f"Port {port} is already in use. Try another one, e.g. PORT={port + 1} python3 app.py")
        else:
            print(f"Could not start server: {exc}")
        return 1

    url = f"http://localhost:{port}"
    ip = lan_address()
    print("=" * 58)
    print("  JAYNE & KIRBY'S WEINER SLOTS - Wiener Dog Jackpot")
    print(f"  Serving {BASE_DIR}")
    print(f"  On this computer: {url}")
    if host in ("0.0.0.0", "::"):
        print(f"  On a phone (same Wi-Fi): http://{ip}:{port}")
        print("  If the phone can't connect, allow Python through the firewall.")
    print("  Press Ctrl+C to stop")
    print("=" * 58)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server. Good dog!")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
