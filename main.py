import webview
from src.backend.mainform import WebUI_api, get_path, config, server

path = get_path.get_path('config.ini', use_mei_pass=False)
cfg = config.config(path)
port = cfg.read_config('server', 'port') or 25432


def get_mainwindow_config():
    a = cfg.get_config([
        {"section": "main", "option": "width"},
        {"section": "main", "option": "height"},
        {"section": "main", "option": "x"},
        {"section": "main", "option": "y"},
        {"section": "main", "option": "maximized"},
    ])

    return {
        "width": int(a["main"]["width"]) if a["main"]["width"] else None,
        "height": int(a["main"]["height"]) if a["main"]["height"] else None,
        "x": int(a["main"]["x"]) if a["main"]["x"] else None,
        "y": int(a["main"]["y"]) if a["main"]["y"] else None,
        "maximized": a["main"]["maximized"] == "True",
    }


if __name__ == '__main__':
    server = server.Server()
    # 创建窗口并加载 HTML 页面
    width, height, x, y, maximized = get_mainwindow_config().values()
    window = webview.create_window(
        '蓝牙心率监测',
        url=f'http://127.0.0.1:{port}/main',
        width=width or 816,  # 800 + 16
        height=height or 642,  # 600 + 28 +16
        x=x,
        y=y,
        maximized=maximized,
        min_size=(450 + 16, 300 + 44),
        shadow=False,
    )

    api = WebUI_api.WebUI_api(window, server)

    window.events.moved += api.on_moved
    window.events.resized += api.on_resized
    window.events.maximized += api.on_maximized
    window.events.restored += api.on_restored
    window.events.closed += api.on_closed

    webview.start()
