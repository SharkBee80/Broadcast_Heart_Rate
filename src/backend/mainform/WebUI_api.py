import random

import threading
import time

from src.backend.mainform import Device_handle, Web_page, Float_window

ble = Device_handle.Device_handle()
web = Web_page.Web_page()
float_window = Float_window.FloatWindow()


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
        float_window.init(window)

        self.window.expose(self.refresh_devices, self.set_device, self.connect_device, self.disconnect_device,
                           self.onload_init)

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

    def on_closed(self):
        ble.disconnect_device()
        float_window.on_closed()
