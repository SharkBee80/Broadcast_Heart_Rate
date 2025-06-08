* 安装

```shell
pip install pyinstaller
```

> pip -r requirements.txt
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
---

* 打包了哪些模块
```shell
pyi-archive_viewer dist/HeartRate.exe
```

---

> pyinstaller -F --clean --add-data="src;src" --hidden-import=webview --hidden-import=bleak --name HeartRate -i heartrate.ico main.py
