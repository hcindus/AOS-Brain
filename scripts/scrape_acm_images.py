#!/usr/bin/env python3
"""
Scrape ACM product images for the Ribbon & Toner catalog + save them to the website.

Image URL pattern (verified): https://www.acmtech.com/assets/images/product-images/{sku[:2]}/{sku}.jpg
Each is a 600x600 JPEG.

Usage:
  python3 scrape_acm_images.py              # full run (resumable)
  python3 scrape_acm_images.py --limit 20   # test a subset
  python3 scrape_acm_images.py --reset      # clear state + start fresh
"""
import json, os, re, time, sys, subprocess, argparse

BASE = "https://www.acmtech.com"
CATALOG = "/root/.openclaw/workspace/acm-catalog/products-catalog.json"
OUTDIR = "/var/www/psdepot.com/assets/images/products"
STATE = "/root/.openclaw/workspace/datadepot/data/acm_image_scrape_state.json"
DELAY = 0.4  # seconds between requests (be a good citizen)


def load_catalog():
    return json.load(open(CATALOG))["products"]


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"done": [], "failed": []}


def save_state(state):
    json.dump(state, open(STATE, "w"), indent=2)


def image_url(sku):
    return f"{BASE}/assets/images/product-images/{sku[:2]}/{sku}.jpg"


def is_valid_image(path):
    """Basic magic-byte check that the downloaded file is a real image."""
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        return False
    with open(path, "rb") as f:
        head = f.read(4)
    return head[:2] == b"\xff\xd8" or head[:4] == b"\x89PNG" or head[:3] == b"GIF"


def download(sku, outpath):
    r = subprocess.run(
        ["curl", "-sL", "-o", outpath, "-w", "%{http_code} %{size_download}", image_url(sku)],
        capture_output=True, text=True, timeout=60,
    )
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Only process N items")
    ap.add_argument("--reset", action="store_true", help="Clear scrape state")
    args = ap.parse_args()

    if args.reset and os.path.exists(STATE):
        os.remove(STATE)

    prods = load_catalog()
    state = load_state()
    done = set(state["done"])
    failed = set(state["failed"])
    os.makedirs(OUTDIR, exist_ok=True)

    todo = [p for p in prods if p["sku"] not in done and p["sku"] not in failed]
    if args.limit:
        todo = todo[: args.limit]

    print(f"catalog={len(prods)} done={len(done)} failed={len(failed)} todo={len(todo)}")

    for i, p in enumerate(todo):
        sku = p["sku"]
        outpath = os.path.join(OUTDIR, f"{sku}.jpg")
        code_size = download(sku, outpath)
        if is_valid_image(outpath):
            state["done"].append(sku)
        else:
            state["failed"].append(sku)
            if os.path.exists(outpath):
                os.remove(outpath)
        time.sleep(DELAY)
        if (i + 1) % 25 == 0:
            save_state(state)
            print(f"  {i+1}/{len(todo)}  done={len(state['done'])} failed={len(state['failed'])}")

    save_state(state)
    print(f"COMPLETE: done={len(state['done'])} failed={len(state['failed'])}")


if __name__ == "__main__":
    main()
