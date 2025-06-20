import webview
from src.backend.mainform import WebUI_api, config, server

port = config.get_config('server', 'port') or 25432


if __name__ == '__main__':
    webview.logger.disabled = True
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False

    server = server.Server()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        url=f'http://127.0.0.1:{port}/main',
        width=816,  # 800 + 16
        height=642,  # 600 + 28 +16
        resizable=False
    )

    api = WebUI_api.WebUI_api(window, server)

    window.events.closed += api.on_closed

    webview.start(debug=False, gui='edgechromium')  # type: ignore
