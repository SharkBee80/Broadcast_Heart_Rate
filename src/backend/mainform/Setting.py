from typing import Optional

import webview

from src.backend.mainform import get_path, config, Float_window

get_path = get_path.get_path
float_window = Float_window.FloatWindow()
cfg = config.WriteConfig()


class Setting:
    def __init__(self):
        self.window: Optional[webview.Window] = None

    def init(self, window):
        self.window = window
        self.window.expose(self.save_setting)

    def load_setting(self):
        server_address = config.get_config('server', 'host')
        server_port = config.get_config('server', 'port')
        float_open = config.get_config('float', 'open')
        self.window.evaluate_js(f"set_text('server_host','{server_address}')")
        self.window.evaluate_js(f"set_text('server_port','{server_port}')")
        if float_open == 'True':
            self.window.evaluate_js("set_switch('open', true)")
            self.window.evaluate_js("set_switch('float_open', true)")

    def save_setting(self, value_json):
        for _json in value_json:
            # print(_json['section'], _json['option'], _json['value'])
            cfg.set_options(_json['section'], _json['option'], _json['value'].__str__())
        JS_ = """
            alert('保存成功\\n请重新启动软件');
            //var x = confirm('保存成功\\n请重新启动软件');
            //if (x == true) {pywebview.api.reboot();}
        """
        self.window.evaluate_js(JS_)
