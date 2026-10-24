# Sony A7M2 AI MOD

索尼 A7M2 双屏摄影辅助原型。**当前 V0.1 仅实现视频输入、浏览器双屏预览及三分法网格**。AI 人眼识别、姿态分析、USB 拍照、自动对焦均未实现。

## Windows P52 快速启动

1. 安装 Python 3.10+，下载本仓库。
2. PowerShell 进入仓库目录：
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8765
   ```
3. 电脑打开 http://127.0.0.1:8765
4. 手机与 P52 接入同一 Wi-Fi，访问 http://<P52局域网IP>:8765（使用 ipconfig 查询）。
5. Windows 防火墙需要允许局域网 TCP 8765；仅在可信局域网运行，本原型没有身份验证。

## A7M2 视频输入

仅有 USB 数据线时，需先确认 Sony Imaging Edge Webcam 在当前 Windows 系统和相机固件上可用，并在系统中呈现为视频采集设备。若无法识别，先用电脑摄像头测试；Micro HDMI 线**不能单独充当采集卡**。可通过环境变量 CAMERA_SOURCE 选择 OpenCV 视频设备索引（默认 0）。

## 限制与安全

当前版本未对 Sony 相机进行固件写入或逆向修改；未测试 A7M2 实机。MJPEG 预览是实验用途，多个客户端各自读取采集设备可能发生争用，下一版将采用单采集线程多客户端广播。请勿将该版本暴露到互联网。
