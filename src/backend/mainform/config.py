import configparser
import os

DEFAULT = "Default"


# 写入配置文件
class config:
    """
    写入config文件\n
    [section] \n
    option = value
    """

    def __init__(self, path):
        """
        :param path: 文件路径
        """
        self.path = path
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path, encoding="utf-8")  # 如果修改，则必须读原文件
        self.init_config()

    def init_config(self):
        if not os.path.exists(self.path):
            self.create_config()

    def reset_config(self):
        self.create_config()

    def create_config(self):
        self.set_config([
            {"section": "server", "option": "host", "value": "127.0.0.1"},
            {"section": "server", "option": "port", "value": "25432"},
            {"section": "start", "option": "refresh", "value": "True"},
            {"section": "float", "option": "open", "value": "False"},
            {"section": "float", "option": "move", "value": "False"},
            {"section": "float", "option": "transparent", "value": "True"},
            {"section": "float", "option": "x", "value": "0"},
            {"section": "float", "option": "y", "value": "774"},
            {"section": "other", "option": "bg-f", "value": "True"}
        ])

    def _with_file(self):
        # write to file
        with open(self.path, "w+", encoding="utf-8") as f:
            self.cf.write(f)  # type: ignore

    def write_config(self, section: str | None, option: str, value: str | bool | None = "") -> None:
        """

        :param section: 类,若为空则使用 "DEFAULT_"
        :param option: 项,若为空则忽略写入
        :param value: 值
        """
        if not section:
            section = DEFAULT
        section = str(section)
        # 写入section值
        if not self.cf.has_section(section):
            self.cf.add_section(section)
        if not option:
            pass
        else:
            if value is None or value == "":
                value = ""
            # 写入option值
            self.cf.set(section, str(option), str(value))
        self._with_file()

    def read_config(self, section: str | None, option: str) -> str | None:
        """

        :param section: 类,若为空则使用 "DEFAULT_"
        :param option: 项,若为空则忽略读取
        :return: 值
        """
        if not section:
            section = DEFAULT
        section = str(section)
        if not option:
            return None
        else:
            try:
                return self.cf.get(section, str(option))
            except configparser.NoSectionError:
                return None
            except configparser.NoOptionError:
                return None

    def remove_config(self, section: str | None, option: str) -> None:
        """
        移除配置项
        :param section: 类,若为空则使用 "DEFAULT_"
        :param option: 项,若为空则忽略移除
        """
        if not section:
            section = DEFAULT
        section = str(section)
        # section 不存在，无需操作
        if not self.cf.has_section(section):
            return
        if option is None:
            pass
        else:
            # 移除option值
            self.cf.remove_option(section, str(option))
        # 移除section值
        if section in self.cf and len(self.cf[section]) == 0:
            self.cf.remove_section(section)
        self._with_file()

    def set_config(self, items: list[dict[str, str]]):
        """
        批量写入配置项
        :param items: list[{"section": "a", "option": "b", "value": "c"}]
        :raises: TypeError 如果输入格式不符合要求
        """
        if not isinstance(items, list):
            raise TypeError("参数 items 必须是列表类型")
        for i in items:
            if not isinstance(i, dict):
                raise TypeError("items 列表中的每个元素必须是字典")
            section = i.get('section')
            option = i.get('option')  # 如果没有 'option' 键，则返回 None
            value = i.get('value')
            self.write_config(section, option, value)

    def get_config(self, items: list[dict[str, str]]) -> dict[str, dict[str, str]]:
        """
        批量读取配置项，并按 section 分类
        :param items: list[{"section": "a", "option": "b"}]
        :return: dict {"a": {"b": "c"}, ...}
        """
        result = {}
        for i in items:
            section = i.get('section') or DEFAULT
            option = i.get('option')
            value = self.read_config(section, option)

            if section not in result:
                result[section] = {}

            if value is not None:
                result[section][option] = value
            else:
                result[section][option] = ""
        return result


if __name__ == '__main__':
    from get_path import get_path

    config = config(get_path("../../config.ini"))

    json_in = [
        {"section": "a", "option": "b", "value": "c"},
        {"section": "a", "option": "d", "value": "e"},
        {"section": "", "option": "g"}
    ]

    json_out = [
        {"section": "a", "option": "b"},
        {"section": "a", "option": "d"},
        {"option": "g"}
    ]
    config.set_config(json_in)
    a = config.get_config(json_out)
    print(a)
