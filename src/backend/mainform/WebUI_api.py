from src.backend.mainform import Device_handle, Web_page, Float_window

ble = Device_handle.Device_handle()
web = Web_page.Web_page()
float_window = Float_window.FloatWindow()


class WebUI_api:
    # 提供给前端调用的方法
    def __init__(self,  window):
        self.window = window

        ble.init(self.window)
        web.init(self.window)
        float_window.init(self.window)

        self.window.expose(self.onload_init)

    def onload_init(self):
        web.set_()

    def on_closed(self):
        ble.disconnect_device()
        float_window.on_closed()
