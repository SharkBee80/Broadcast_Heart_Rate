import random

import webview
import threading
import time

window = None

# 模拟蓝牙数据获取函数
# 心率相关常量
BASE_HEART_RATE = 70  # 基础心率
RATE_VARIATION = 10  # 每次波动最大幅度
MIN_HEART_RATE = 40
MAX_HEART_RATE = 200

# 内部状态变量
_current_heart_rate = BASE_HEART_RATE


def get_bluetooth_heart_rate():
    """
    获取蓝牙设备模拟的心率值（单位：次/分钟）
    心率变化平滑，避免剧烈波动

    返回:
        int: 模拟的心率值，范围在 40 到 200 之间，变化幅度受限
    """
    global _current_heart_rate

    # 在当前心率基础上小幅波动
    variation = random.randint(-RATE_VARIATION, RATE_VARIATION)
    new_rate = max(MIN_HEART_RATE, min(MAX_HEART_RATE, _current_heart_rate + variation))

    _current_heart_rate = new_rate
    return new_rate


class WebUI_api:
    # 提供给前端调用的方法
    _fetch_thread = None
    _fetch_active = False

    def __init__(self):
        pass

    def fetch_heart_rate(self):
        if self._fetch_active:
            return  # 防止重复启动

        self._fetch_active = True

        def _fetch():
            while self._fetch_active:
                rate = get_bluetooth_heart_rate()
                window.evaluate_js(f"updateHeartRate({rate})")
                time.sleep(1)

        self._fetch_thread = threading.Thread(target=_fetch, daemon=True)
        self._fetch_thread.start()

    def stop_fetching(self):
        self._fetch_active = False
        window.evaluate_js(f"updateHeartRate('-- BPM')")
        if self._fetch_thread:
            self._fetch_thread.join()


if __name__ == '__main__':
    api = WebUI_api()
    # 创建窗口并加载 HTML 页面
    window = webview.create_window(
        '蓝牙心率监测',
        './src/frontend/index.html',
        js_api=api,
    )

    webview.start(debug=True, http_server=True, http_port=25432)
