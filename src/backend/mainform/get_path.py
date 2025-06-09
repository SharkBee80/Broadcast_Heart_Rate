import os
import sys


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    out_path = os.path.normpath(os.path.join(base_path, relative_path))
    print(out_path)
    return out_path
