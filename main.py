import webview

from src.backend.mainform import WebUI_api

if __name__ == '__main__':
    webview.logger.disabled = True
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        'http://127.0.0.1:25432/main',
        width=816,  # 800 + 16
        height=642,  # 600 + 28 +16
        resizable=False
    )

    api = WebUI_api.WebUI_api(window)

    window.events.closed += api.on_closed

    webview.start(debug=True, gui='edgechromium')
