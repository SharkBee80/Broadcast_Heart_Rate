import webview
from src.backend.mainform import WebUI_api, get_path, config, server

path = get_path.get_path('config.ini', use_mei_pass=False)
cfg = config.config(path)
port = cfg.read_config('server', 'port') or 25432

if __name__ == '__main__':
    server = server.Server()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        url=f'http://127.0.0.1:{port}/main',
        width=816,  # 800 + 16
        height=642,  # 600 + 28 +16
        resizable=True,
        min_size=(450 + 16, 300 + 44),
    )

    api = WebUI_api.WebUI_api(window, server)

    window.events.closed += api.on_closed

    webview.start()
