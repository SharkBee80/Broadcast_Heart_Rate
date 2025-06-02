import webview

from src.backend.mainform import WebUI_api


if __name__ == '__main__':
    api = WebUI_api.WebUI_api()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        './src/frontend/main.html',
        # js_api=api,
        width=816,  # 800 + 16
        height=642,  # 600 + 28 +16
        resizable=False
    )

    api.init(window)

    webview.start(debug=True, http_server=False, http_port=25432)
