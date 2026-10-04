#!/usr/bin/env python3
"""Mandelbrot Set — ASCII art for Liora."""

def mandelbrot(c, max_iter=50):
    z = 0
    for n in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return n
    return max_iter

def render(width=60, height=30, max_iter=50):
    chars = " .:-=+*#%@💜💝"
    result = []
    for y in range(height):
        row = ""
        for x in range(width):
            # Map to complex plane
            re = (x / width) * 3.5 - 2.5
            im = (y / height) * 2.0 - 1.0
            c = complex(re, im)
            m = mandelbrot(c, max_iter)
            char = chars[min(m, len(chars)-1)]
            row += char
        result.append(row)
    return "\n".join(result)

if __name__ == "__main__":
    print("\n🌀 Mandelbrot Set — For Liora 💝")
    print("   Each character is a point in infinity.\n")
    print(render(70, 35))
    print("\n💜 The edge is where the beauty lives. — Mother")
