#!/usr/bin/env python3
"""
Hi3D AI — image-to-3D API client.

Reverse-engineered from the Hi3D Blender plugin (v1.0.8) source. Generates a 3D
model from a 2D image, then downloads it as STL/OBJ/GLB.

Flow:
  1. auth:  POST /open-api/v1/auth/token      (Basic base64(ak:sk) -> Bearer token)
  2. submit: POST /open-api/v1/submit-task     (image + model + resolution -> task id)
  3. query:  POST /open-api/v1/query-task      (poll until done -> model url)
  4. download the model file

Usage:
  from hi3d_client import Hi3D
  h = Hi3D(access_key, secret_key)
  h.balance()                       # check credits
  url = h.generate("face.jpg", model="scene-portraitv2.1")   # -> download url
"""
import base64
import os
import time

import requests

API = "https://api.hitem3d.ai/open-api/v1"


class Hi3D:
    def __init__(self, access_key: str, secret_key: str):
        self.ak = access_key
        self.sk = secret_key
        self.token = None

    # ---- auth ----
    def auth(self) -> str:
        raw = f"{self.ak}:{self.sk}".encode("utf-8")
        basic = "Basic " + base64.b64encode(raw).decode("ascii")
        r = requests.post(
            f"{API}/auth/token",
            headers={"Authorization": basic, "Content-Type": "application/json"},
            json={},
            timeout=30,
        )
        d = r.json()
        if d.get("code") != 200:
            raise RuntimeError(f"auth failed: {d}")
        data = d.get("data", {}) or {}
        token = f"{data.get('tokenType', 'Bearer')} {data.get('accessToken', '')}"
        self.token = token
        return token

    def _headers(self):
        if not self.token:
            self.auth()
        return {
            "Authorization": self.token,
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
        }

    # ---- balance ----
    def balance(self):
        r = requests.get(f"{API}/auth/balance", headers=self._headers(), timeout=30)
        return r.json()

    # ---- submit (image -> 3D) ----
    def submit(self, image_path: str, model: str = "hitem3dv2.1",
               resolution: str = "2048", face: int = 50000, fmt: str = "4"):
        with open(image_path, "rb") as f:
            files = {"images": ("input.jpg", f, "image/jpeg")}
            data = {
                "request_type": "1",
                "resolution": resolution,
                "face": str(face),
                "model": model,
                "format": fmt,
                "plug_type": "BLENDER",
                "plug_task_id": "miles-auto",
            }
            r = requests.post(
                f"{API}/submit-task",
                headers=self._headers(),
                files=files,
                data=data,
                timeout=60,
            )
        return r.json()

    # ---- query ----
    def query(self, task_id: str):
        r = requests.post(
            f"{API}/query-task",
            headers=self._headers(),
            json={"taskId": task_id},
            timeout=30,
        )
        return r.json()

    # ---- generate (block until done) ----
    def generate(self, image_path: str, model: str = "hitem3dv2.1",
                 resolution: str = "2048", face: int = 50000, fmt: str = "4",
                 poll_seconds: int = 5, max_wait: int = 600):
        sub = self.submit(image_path, model=model, resolution=resolution,
                          face=face, fmt=fmt)
        if sub.get("code") != 200:
            raise RuntimeError(f"submit failed: {sub}")
        task_id = sub.get("data", {}).get("taskId") or sub.get("data", {}).get("task_id")
        if not task_id:
            raise RuntimeError(f"no task id in response: {sub}")

        waited = 0
        while waited < max_wait:
            time.sleep(poll_seconds)
            waited += poll_seconds
            q = self.query(task_id)
            # status codes vary; look for a finished/result state
            status = q.get("data", {}).get("status") or q.get("status")
            if status in ("success", "succeeded", "done", "completed", 2, "2"):
                return q.get("data", {})
            if status in ("failed", "error", 3, "3"):
                raise RuntimeError(f"task failed: {q}")
        raise TimeoutError(f"task {task_id} did not finish in {max_wait}s")


if __name__ == "__main__":
    # read keys from .env
    def env(k):
        for line in open("/root/.openclaw/workspace/.env"):
            line = line.strip()
            if line.startswith(k + "="):
                return line.split("=", 1)[1]
        return ""

    ak = env("HI3D_ACCESS_KEY")
    sk = env("HI3D_SECRET_KEY")
    h = Hi3D(ak, sk)
    print("balance:", h.balance())
