* 查看所有包

```shell
pip freeze
```

* 卸载所有包

```shell
pip uninstall -y -r packages.txt
pip cache purge
```
* 升级
```shell
python.exe -m pip install --upgrade pip
```
* 安装

```shell
pip install pyinstaller
```

```shell
pip install -r requirements.txt
```

---

* 打包

```shell
pyinstaller HeartRate.spec
```

/ 无终端

```shell
pyinstaller -F -w --clean --add-data="src;src" --exclude-module=PyQt5 --name HeartRate -i heartrate.ico main.py
```

/ 终端

```shell
pyinstaller -F --clean --add-data="src;src" --exclude-module=PyQt5 --name HeartRate_with_terminal -i heartrate.ico main.py
```

/

```shell
pyinstaller -F -w --clean --add-data="src;src" --exclude-module=PyQt5 --additional-hooks-dir=. --noconfirm --name HeartRate -i heartrate.ico main.py
```

---

* 打包了哪些模块

```shell
pyi-archive_viewer dist/HeartRate.exe
```

---

> pyinstaller -F --clean --add-data="src;src" --hidden-import=webview --hidden-import=bleak --name HeartRate -i
> heartrate.ico main.py
