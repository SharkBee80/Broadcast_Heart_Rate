import os
import sys
from pathlib import Path


def get_program_name():
    program_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    return str(program_name)


def get_path(relative_path: str, output_type: str = "str", config_dir: str = "", use_mei_pass: bool = True,
             create_base_dir: bool = True):
    """
    获取相对于 base_path 的路径。

    :param relative_path: 相对路径字符串
    :param output_type: "str" or Path
    :param config_dir: 配置文件夹（用于打包环境,配置文件）
    :param use_mei_pass: 是否强制使用 sys._MEIPASS（用于打包环境,temp文件）
    :param create_base_dir: 新建基础文件夹
    :return: 组合后的绝对路径
    """
    if isPkg():
        if not use_mei_pass:  # 打包后
            config_dir = config_dir or get_program_name() + "_config"
            base_path = Path(sys.executable).parent / config_dir  # exe所在目录
            created = False
            if not base_path.exists() and create_base_dir:
                base_path.mkdir(parents=True, exist_ok=True)
                created = True
            descript = f".这里是{get_program_name()}的配置文件"
            if created:
                try:
                    with open(base_path / descript, "w", encoding="utf-8") as f:
                        f.write("")  # 可选：写入初始内容
                except (IOError, OSError) as e:
                    print(f"无法创建配置文件: {e}")
        else:
            base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(sys.argv[0]).parent.resolve() / config_dir

    try:
        out_path = (base_path / relative_path).resolve(strict=False)
    except (PermissionError, OSError) as e:
        raise RuntimeError(f"无法解析路径: {e}") from e

    if output_type == "str":
        return str(out_path)
    else:
        return Path(out_path)


def isPkg() -> bool:
    if getattr(sys, 'frozen', False):
        return True
    else:
        return False


if __name__ == "__main__":
    # 示例：获取 data.json 的绝对路径
    print(get_path("data.json"))
