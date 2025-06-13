import configparser
import os
import textwrap
from src.backend.mainform.get_path import get_path


def create_config():
    """
    config = configparser.ConfigParser()
    # 设置server部分
    config['server'] = {
        'host': '0.0.0.0',
        'port': '25432',
    }
    """

    configf = textwrap.dedent("""\
    # 设置server部分
    [server]
    host = 0.0.0.0
    port = 25432

    # 浮窗
    [float]
    open = False
    x = 0
    y = 774\
""")
    # 写入到文件
    with open(config_path, 'w', encoding='utf-8') as configfile:
        # config.write(configfile)  # type: ignore
        configfile.write(configf)


def init_config():
    if not os.path.exists(config_path):
        create_config()


def reset_config():
    create_config()


def read_config():
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


def get_config(section, option):
    config = read_config()
    return config.get(section, option)


# 写入配置文件
class WriteConfig:
    """写入config文件"""

    def __init__(self):
        self.filename = config_path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.filename,  encoding="utf-8")  # 如果修改，则必须读原文件

    def _with_file(self):
        # write to file
        with open(self.filename, "w+",  encoding="utf-8") as f:
            self.cf.write(f)  # type: ignore

    def add_section(self, section):
        # 写入section值
        self.cf.add_section(section)
        self._with_file()

    def set_options(self, section, option, value=None):
        """写入option值"""
        self.cf.set(section, option, value)
        self._with_file()

    def remove_section(self, section):
        """移除section值"""
        self.cf.remove_section(section)
        self._with_file()

    def remove_option(self, section, option):
        """移除option值"""
        self.cf.remove_option(section, option)
        self._with_file()


if __name__ == '__main__':
    config_path = get_path('../config.ini')
    reset_config()

    host = get_config('server', 'host')
    port = get_config('server', 'port')

    print("Server 数据:")
    print(f"Host: {host}")
    print(f"Port: {port}")
else:
    config_path = get_path('src/backend/config.ini')
    init_config()
