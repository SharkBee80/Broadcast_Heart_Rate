import random

import webview
import threading
import time

from src.backend.mainform.WebUI_api import WebUI_api


if __name__ == '__main__':
    api = WebUI_api()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        './src/frontend/main.html',
        # js_api=api,
        resizable=False
    )
    api.init(window)

    webview.start(debug=False, http_server=False, http_port=25432)
