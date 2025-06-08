import threading
import time
from flask import Flask, render_template, jsonify, send_from_directory

import config

import logging

log = logging.getLogger('werkzeug')
log.disabled = True

port = config.API['port']


class Server:
    static_folder = '../../frontend/static'
    template_folder = '../../frontend/template'

    def __init__(self):
        self.app = Flask(__name__, static_folder=self.static_folder, template_folder=self.template_folder)

        self.app.add_url_rule('/', 'root', self.root)
        self.app.add_url_rule('/main', 'main', self.main)
        self.app.add_url_rule('/api', 'api', self.api)

        self.app.add_url_rule('/<path:filename>', 'html', self.html)

        self.app.register_error_handler(404, self.page_not_found)

        self.rate = None
        self.old_time = 0

        self.run()

    '''route'''

    def root(self):
        return render_template('index.html')

    def main(self):
        return render_template('main.html')

    def api(self):
        return jsonify({'rate': self.calc_rate()})

    def html(self, filename):
        return send_from_directory(self.template_folder, filename)

    def page_not_found(self, error):
        return jsonify({'error': '404'}), 404

    '''function'''

    def set_rate(self, rate):
        self.rate = rate
        self.old_time = time.time()

    def calc_rate(self):
        if time.time() - self.old_time > 3:
            return ''
        return self.rate

    def run(self):
        server_thread = threading.Thread(target=self.app_run, daemon=True)
        server_thread.start()
        print(f'Server started at: \n * http://127.0.0.1:{port}')

    def app_run(self):
        self.app.run('0.0.0.0', port)


if __name__ == '__main__':
    server = Server()
    server_ = threading.Thread(target=server.run, daemon=True)
    server_.start()
