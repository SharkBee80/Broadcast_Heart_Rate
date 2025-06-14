# Broadcast Heart Rate / 心率广播

## 介绍
一个用于接收心率广播的python程序

[https://github.com/SharkBee80/Broadcast_Heart_Rate](https://github.com/SharkBee80/Broadcast_Heart_Rate)

使用 `pywebview`.`bleak`.`flask` 模块

## 图片
<div>
    <img alt="img.png" height="170" src="files/0.png"/>
    <img alt="img.png" height="170" src="files/1.png"/>
    <img alt="img.png" height="170" src="files/2.png"/>
    <img alt="img.png" height="170" src="files/3.png"/>
    <img alt="img.png" height="170" src="files/4.png"/>
    <img alt="img.png" height="170" src="files/5.png"/>
    <img alt="img.png" height="170" src="files/3-1.png">
    <img alt="img.png" height="170" src="files/obs.png">
</div>

## 缺陷
1. 悬浮窗无法设置透明、缩放
2. 要修改悬浮窗内容需自行打包
3. UI
4. ……

## 使用
* 自行摸索

## 安装
### pyinstaller
```shell
pip install pyinstaller
```
---
### 依赖
```shell 
pip -r requirements.txt
```
---
### 打包
```shell
pyinstaller HeartRate.spec
```
###### or
```shell
pyinstaller -F -w --clean --add-data="src;src" --name HeartRate -i heartrate.ico main.py
```

## [LICENSE](LICENSE)
* [GPL-3.0](https://opensource.org/license/gpl-3-0)
<div>
    <img width="170" src="files/licenses.png">
</div>
