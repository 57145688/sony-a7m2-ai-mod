import asyncio
import os
import threading
import time

import cv2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="Sony A7M2 AI MOD")
cap = None
lock = threading.Lock()
source = os.getenv("CAMERA_SOURCE", "0")
try:
    source = int(source)
except ValueError:
    pass

def frames():
    global cap
    while True:
        with lock:
            if cap is None or not cap.isOpened():
                cap = cv2.VideoCapture(source, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
            ok, frame = cap.read() if cap.isOpened() else (False, None)
        if not ok:
            import numpy as np
            frame = np.zeros((480, 854, 3), dtype=np.uint8)
            cv2.putText(frame, "NO CAMERA - check USB/webcam mode", (55, 230),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            time.sleep(0.3)
        else:
            frame = cv2.resize(frame, (854, 480))
        h, w = frame.shape[:2]
        for x in (w // 3, 2 * w // 3):
            cv2.line(frame, (x, 0), (x, h), (190, 190, 190), 1)
        for y in (h // 3, 2 * h // 3):
            cv2.line(frame, (0, y), (w, y), (190, 190, 190), 1)
        _, jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"

@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html><html lang="zh"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>A7M2 AI MOD</title><style>body{background:#111;color:#eee;font-family:system-ui;margin:20px}
    img{width:100%;max-width:1100px;border:1px solid #444}small{color:#aaa}</style>
    <h2>Sony A7M2 AI MOD · V0.1</h2><img src="/video" alt="实时取景">
    <p>双屏实时预览 · 三分法构图网格</p><small>AI 检测与 USB 快门控制尚未接入；请勿将本版视为自动追焦功能。</small></html>"""

@app.get("/video")
def video():
    return StreamingResponse(frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/health")
def health():
    return {"status": "ok", "camera_source": str(source)}
