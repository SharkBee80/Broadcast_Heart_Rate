import webview
from typing import Optional
from src.backend.mainform import get_path, config, Float_window

float_window = Float_window.FloatWindow()
path = get_path.get_path('config.ini', use_mei_pass=False)
cfg = config.config(path)


class Setting:
    def __init__(self):
        self.window: Optional[webview.Window] = None

    def init(self, window):
        self.window = window
        self.window.expose(self.save_setting, self.reset_setting)

    def load_setting(self):
        # server
        server_address = cfg.read_config('server', 'host') or '127.0.0.1'
        server_port = cfg.read_config('server', 'port') or 25432
        self.window.evaluate_js(f"set_text('server_host','{server_address}')")
        self.window.evaluate_js(f"set_text('server_port','{server_port}')")
        # start
        start_refresh = cfg.read_config('start', 'refresh')
        if start_refresh == 'True':
            self.window.evaluate_js("refresh_devices()")
            self.window.evaluate_js("set_switch('start_refresh', true)")
        # float
        float_open = cfg.read_config('float', 'open')
        float_move = cfg.read_config('float', 'move')
        float_transparent = cfg.read_config('float', 'transparent')
        if float_open == 'True':
            self.window.evaluate_js("set_switch('open', true)")
            self.window.evaluate_js("set_switch('float_open', true)")
        if float_move == 'True':
            self.window.evaluate_js("set_switch('move', true)")
        if float_transparent == 'True':
            self.window.evaluate_js("set_switch('transparent', true)")

    def save_setting(self, value_json):
        cfg.set_config(value_json)
        self.after_change()

    def reset_setting(self):
        cfg.reset_config()
        self.after_change()

    def after_change(self):
        JS_ = """
            alert('保存成功\\n请重新启动软件');
            //var x = confirm('保存成功\\n请重新启动软件');
            //if (x == true) {pywebview.api.reboot();}
        """
        self.window.evaluate_js(JS_)

    '''
    import subprocess
    import sys
    def reboot(self):
        # 获取当前执行路径和参数
        executable = sys.executable
        args = sys.argv[:]

        # 添加延迟确保当前进程退出后再启动新进程
        self.window.destroy()  # 关闭当前窗口

        # 启动新进程
        if sys.platform == 'win32':
            subprocess.Popen([executable] + args, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([executable] + args)

        # 退出当前进程
        sys.exit(0)
    '''
