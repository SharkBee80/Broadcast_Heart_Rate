```shell
pip install pyinstaller
```
#### pip -r requirements.txt

```shell
pyinstaller HeartRate.spec
```

```shell
pyinstaller -F -w --clean --add-data="src;src" --name HeartRate -i heartrate.ico main.py
```

---

>pyinstaller -F --clean --add-data="src;src" --hidden-import=webview --hidden-import=bleak --name HeartRate -i heartrate.ico main.py
