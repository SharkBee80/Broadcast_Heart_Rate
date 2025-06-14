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
        self.window.expose(self.save_setting, self.reset_setting)

    def load_setting(self):
        # server
        server_address = config.get_config('server', 'host')
        server_port = config.get_config('server', 'port')
        self.window.evaluate_js(f"set_text('server_host','{server_address}')")
        self.window.evaluate_js(f"set_text('server_port','{server_port}')")
        # start
        start_refresh = config.get_config('start', 'refresh')
        if start_refresh == 'True':
            self.window.evaluate_js("refresh_devices()")
            self.window.evaluate_js("set_switch('start_refresh', true)")
        # float
        float_open = config.get_config('float', 'open')
        float_move = config.get_config('float', 'move')
        float_transparent = config.get_config('float', 'transparent')
        if float_open == 'True':
            self.window.evaluate_js("set_switch('open', true)")
            self.window.evaluate_js("set_switch('float_open', true)")
        if float_move == 'True':
            self.window.evaluate_js("set_switch('move', true)")
            self.window.evaluate_js("set_switch('float_move', true)")
        if float_transparent == 'True':
            self.window.evaluate_js("set_switch('transparent', true)")
            self.window.evaluate_js("set_switch('float_transparent', true)")

    def save_setting(self, value_json):
        for _json in value_json:
            # print(_json['section'], _json['option'], _json['value'])
            cfg.set_options(_json['section'], _json['option'], _json['value'].__str__())
        self.after_change()

    def reset_setting(self):
        config.reset_config()
        self.after_change()

    def after_change(self):
        JS_ = """
            alert('保存成功\\n请重新启动软件');
            //var x = confirm('保存成功\\n请重新启动软件');
            //if (x == true) {pywebview.api.reboot();}
        """
        self.window.evaluate_js(JS_)
