import random

import threading
import time

from src.backend.mainform import Device_handle, Web_page

ble = Device_handle.Device_handle()
web = Web_page.Web_page()

# 模拟蓝牙数据获取函数
# 心率相关常量
BASE_HEART_RATE = 70  # 基础心率
RATE_VARIATION = 6  # 每次波动最大幅度
MIN_HEART_RATE = 40
MAX_HEART_RATE = 165

# 内部状态变量
_current_heart_rate = BASE_HEART_RATE


def get_bluetooth_heart_rate():
    """
    获取蓝牙设备模拟的心率值（单位：次/分钟）
    心率变化平滑，避免剧烈波动

    返回:
        int: 模拟的心率值，范围在 40 到 200 之间，变化幅度受限
    """
    global _current_heart_rate

    # 在当前心率基础上小幅波动
    variation = random.randint(-RATE_VARIATION, RATE_VARIATION)
    new_rate = max(MIN_HEART_RATE, min(MAX_HEART_RATE, _current_heart_rate + variation))

    _current_heart_rate = new_rate
    return new_rate


class WebUI_api:
    # 提供给前端调用的方法
    def __init__(self):
        self._fetch_thread = None
        self._fetch_active = False
        self._fetch_event = threading.Event()  # 使用线程事件替代布尔标志
        self.window = None
        pass

    def init(self, window):
        self.window = window
        ble.init(window)
        web.init(window)
        self.window.expose(self.refresh_devices, self.set_device, self.connect_device, self.disconnect_device, self.onload_init, self.open_in_browser)

    def refresh_devices(self):
        ble.refresh_devices()

    def set_device(self, device):
        ble.set_device(device)

    def connect_device(self):
        ble.connect_device()

    def disconnect_device(self):
        ble.disconnect_device()

    def onload_init(self):
        web.set_()

    def open_in_browser(self, url):
        web.open_in_browser(url)

    def on_closed(self):
        ble.disconnect_device()

    def fetch_heart_rate(self):
        if self._fetch_event.is_set():
            print("[INFO] Heart rate fetching already active.")
            return  # 防止重复启动

        self._fetch_event.set()

        def _fetch():
            try:
                while self._fetch_event.is_set():
                    rate = get_bluetooth_heart_rate()
                    self.window.evaluate_js(f"updateHeartRate({rate})")
                    time.sleep(1)
            except Exception as e:
                print(f"[ERROR] Heart rate fetching error: {e}")

        self._fetch_thread = threading.Thread(target=_fetch, daemon=True)
        self._fetch_thread.start()

    def stop_fetching(self):
        try:
            self._fetch_event.clear()
            if self.window:
                self.window.evaluate_js(f"updateHeartRate('-- BPM')")
            if self._fetch_thread and self._fetch_thread.is_alive():
                self._fetch_thread.join()
            else:
                print("[INFO] No active heart rate fetching thread found.")
        except Exception as e:
            print(f"[ERROR] Error stopping heart rate fetching: {e}")
