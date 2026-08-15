#!/usr/bin/env python3
"""Generate the PWA icons (no image libraries needed).

Draws a teal rounded square with a perforated pickleball on it, supersampled
4x for smooth edges, and writes the PNGs into ../icons/.

    python3 tools/make-icons.py
"""

import math
import struct
import zlib
from pathlib import Path

SS = 4  # supersample factor
TEAL = (15, 118, 110)
BALL = (222, 232, 90)
HOLE = (150, 168, 40)
OUT = Path(__file__).resolve().parent.parent / "icons"


def blend(dst, src, alpha):
    return tuple(round(d + (s - d) * alpha) for d, s in zip(dst, src))


def coverage(px, py, shape):
    """Fraction of a pixel covered, sampled on an SS x SS grid."""
    hits = 0
    for sy in range(SS):
        for sx in range(SS):
            if shape(px + (sx + 0.5) / SS, py + (sy + 0.5) / SS):
                hits += 1
    return hits / (SS * SS)


def make(size, *, maskable=False):
    pad = 0 if maskable else size * 0.0
    radius = size * 0.22
    cx = cy = size / 2
    # Maskable icons get cropped to a circle by the launcher, so shrink the art.
    ball_r = size * (0.26 if maskable else 0.30)
    hole_r = size * 0.035
    holes = [
        (cx + ball_r * 0.45 * math.cos(a), cy + ball_r * 0.45 * math.sin(a))
        for a in [math.radians(d) for d in (25, 100, 175, 250, 325)]
    ] + [(cx, cy)]

    def in_rounded_square(x, y):
        if x < pad or y < pad or x > size - pad or y > size - pad:
            return False
        dx = max(pad + radius - x, 0, x - (size - pad - radius))
        dy = max(pad + radius - y, 0, y - (size - pad - radius))
        return dx * dx + dy * dy <= radius * radius

    def in_ball(x, y):
        return (x - cx) ** 2 + (y - cy) ** 2 <= ball_r * ball_r

    rows = []
    for y in range(size):
        row = bytearray([0])  # PNG filter byte: none
        for x in range(size):
            bg_a = coverage(x, y, in_rounded_square)
            color = blend((255, 255, 255), TEAL, bg_a)
            color = blend(color, BALL, coverage(x, y, in_ball))
            for hx, hy in holes:
                a = coverage(x, y, lambda px, py, hx=hx, hy=hy: (px - hx) ** 2 + (py - hy) ** 2 <= hole_r * hole_r)
                if a:
                    color = blend(color, HOLE, a)
            row += bytes(color)
            row += bytes([round(255 * (1 if maskable else bg_a))])
        rows.append(bytes(row))
    return b"".join(rows)


def write_png(path, size, raw):
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    path.write_bytes(png)
    print(f"{path.name}  {len(png):,} bytes")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for size in (180, 192, 512):
        write_png(OUT / f"icon-{size}.png", size, make(size))
    write_png(OUT / "icon-maskable-512.png", 512, make(512, maskable=True))
