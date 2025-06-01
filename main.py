import webview
import threading
import time


# 模拟蓝牙数据获取函数
def get_bluetooth_heart_rate():
    """
    获取蓝牙设备模拟的心率值（单位：次/分钟）

    返回:
        int: 模拟的心率值，范围在 40 到 200 之间
    """
    heart_rate = int(time.time() % 161) + 40
    return heart_rate


# 提供给前端调用的方法
_fetch_thread = None
_fetch_active = False


class WebUI_api:
    def __init__(self):
        pass

    def fetch_heart_rate(self):
        global _fetch_thread, _fetch_active

        if _fetch_active:
            return  # 防止重复启动

        _fetch_active = True

        def _fetch():
            while _fetch_active:
                rate = get_bluetooth_heart_rate()
                #evaluate_js(f"updateHeartRate({rate})")

                time.sleep(1)

        _fetch_thread = threading.Thread(target=_fetch, daemon=True)
        _fetch_thread.start()

    def stop_fetching(self):
        global _fetch_active
        _fetch_active = False


if __name__ == '__main__':
    api = WebUI_api()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        './src/frontend/index.html',
        js_api=api,
    )

    webview.start(debug=False, http_server=True, http_port=25432, )
