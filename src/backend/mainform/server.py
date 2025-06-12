import json
import threading
import time
from flask import Flask, render_template, jsonify, send_from_directory, Response
from flask_cors import CORS

import logging

from src.backend.mainform import get_path, config

log = logging.getLogger('werkzeug')
log.disabled = True

get_path = get_path.get_path
host = config.get_config('server', 'host')
port = config.get_config('server', 'port')


class Server:
    static_folder = get_path('src/frontend/static')
    template_folder = get_path('src/frontend/template')
    web_folder = get_path('src/frontend/web')

    def __init__(self):
        self.app = Flask(__name__, static_folder=self.static_folder, template_folder=self.template_folder)

        # r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
        CORS(self.app, resources=r'/*')
        '''route'''
        self.app.add_url_rule('/', 'root', self.root)
        self.app.add_url_rule('/main', 'main', self.main)
        '''api'''
        self.app.add_url_rule('/api', 'api', self.api)

        self.app.add_url_rule('/sse1', 'sse1', self.sse1)
        self.app.add_url_rule('/sse2', 'sse2', self.sse2)
        '''path'''
        self.app.add_url_rule('/<path:filename>', 'html', self.html)
        self.app.add_url_rule('/web/<path:filename>', 'web', self.web)

        self.app.register_error_handler(404, self.page_not_found)

        self.rate = None
        self.old_time = 0
        self.data_condition = threading.Condition()

        self.run()

    '''route'''

    def root(self):
        return render_template('index.html')

    def main(self):
        return render_template('main.html')

    def api(self):
        return jsonify(self.json_out())

    def sse1(self):
        def event_stream():
            while True:
                yield f"data: {self.json_out()}\n\n"
                time.sleep(1)

        return Response(
            event_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )

    def sse2(self):
        def event_stream():
            while True:
                with self.data_condition:
                    self.data_condition.wait()
                    yield f"data: {self.json_out()}\n\n"

        return Response(
            event_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )

    def html(self, filename):
        return send_from_directory(self.template_folder, filename)

    def web(self, filename):
        return send_from_directory(self.web_folder, filename)

    def page_not_found(self, error):
        return jsonify({'error': '404'}), 404

    '''function'''

    def set_rate(self, rate):
        with self.data_condition:
            if rate != self.rate:
                self.data_condition.notify_all()
            self.old_time = time.time()
            self.rate = rate

    def calc_rate(self):
        if time.time() - self.old_time > 5:
            return ["", 'N']
        return [self.rate, 'Y']

    def json_out(self):
        a = self.calc_rate()
        j = {
            "rate": a[0],
            "time": time.strftime('%H:%M:%S'),
            "OK": a[1]
        }
        return json.dumps(j)

    def run(self):
        server_thread = threading.Thread(target=self.app_run, daemon=True)
        server_thread.start()
        print(f'Server started at: \n * http://{host}:{port}')

    def app_run(self):
        self.app.run(host, port)


if __name__ == '__main__':
    server = Server()
    server_ = threading.Thread(target=server.run, daemon=True)
    server_.start()
