from threading import Timer


class timer_:
    def __init__(self, delay: float):
        """

        :param delay: s
        """
        self.delay = delay
        self.timer = None

    def task(self, callback, *args):
        """每次调用会取消之前的定时任务，并重新开始计时"""
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.delay, callback, args)
        self.timer.daemon = True  # 守护线程，避免阻塞主程序退出
        self.timer.start()

    def cancel(self):
        """取消定时任务"""
        if self.timer:
            self.timer.cancel()
