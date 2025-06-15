import json
import time
import webview
import asyncio
from typing import Optional
from bleak import BleakScanner, BleakClient

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")  # 黄色
# 心率服务UUID（标准特征值）
HEART_RATE_SERVICE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


class Device_handle:
    """
    This class is used to handle the device.
    """

    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.server = None

        self._set_device = None
        self.client: Optional[BleakClient] = None
        self.heart_rate_char = None
        self.heart_rate = None

        self.disconnect_event: Optional[asyncio.Event] = None

    def init(self, window, server):
        self.window = window
        self.server = server
        self.window.expose(self.refresh_devices, self.set_device, self.connect_device, self.disconnect_device)

    def refresh_devices(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.scan_devices())
            loop.run_until_complete(asyncio.sleep(0.1))  # 给事件处理一点时间
        finally:
            loop.close()

    async def scan_devices(self):
        """开始扫描蓝牙设备"""
        try:
            self.window.evaluate_js("ButtonState('refresh_devices',false,'刷新中...')")
            logging.info("正在扫描蓝牙设备...")
            devices = await BleakScanner.discover()
            devices_data = [
                {'name': d.name, 'address': d.address, 'rssi': d.rssi}
                for d in devices
                if d.name is not None and d.name.strip()
            ]
            devices_data.sort(key=lambda x: x['rssi'] if x['rssi'] is not None else -999, reverse=True)
            # 排序后统一转换为字符串
            for device in devices_data:
                device['rssi'] = f"{device['rssi']}dBm"  # type: ignore

            print(f"发现 {len(devices_data)} 个设备")
            logging.info(f"设备列表: {devices_data}")
            self.window.evaluate_js(f"update_devices({json.dumps(devices_data, ensure_ascii=False)})")
        except Exception as e:
            logging.warning(f"扫描时发生错误: {e}")
        finally:
            self.window.evaluate_js("ButtonState('refresh_devices',true,'刷新')")

    def set_device(self, device):
        self._set_device = device
        logging.info(f"{device}")

    def connect_device(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.connect())
            loop.run_until_complete(asyncio.sleep(0.1))  # 给事件处理一点时间
        except Exception as e:
            logging.warning(f"连接时发生错误: {e}")
        finally:
            loop.close()

    async def connect(self):
        """连接选定设备"""
        selected = self._set_device
        if not selected:
            logging.warning("未选择任何设备")
            return
        if self.client and self.client.is_connected:
            logging.warning(f"已连接: {self.client.address}")
            return
        address = selected['address']
        logging.info(f"正在连接: {address}")

        try:
            self.window.evaluate_js("ButtonState('connect_device',false,'连接中...')")
            self.client = BleakClient(address, disconnected_callback=self.disconnected_callback, timeout=5)

            await asyncio.wait_for(self.client.connect(), timeout=5)

            if self.client.is_connected:
                logging.info(f"已连接: {address}")
                '''成功'''
                self.window.evaluate_js("ButtonState('connect_device',false,'已连接')")
                self.window.evaluate_js("ListState(false)")
                self.window.evaluate_js("document.querySelectorAll('.choice a')[2].click()")
                self.window.run_js("startHeartRate(true)")
                # 启用心率通知
                self.disconnect_event = asyncio.Event()
                await self.enable_heart_rate_notifications()
            else:
                logging.warning(f"无法连接: {address}")
                self.window.evaluate_js("ButtonState('connect_device',true,'连接')")
        except asyncio.TimeoutError:
            logging.warning(f"连接超时: {address}")
            self.window.evaluate_js("ButtonState('connect_device',true,'连接')")
        except Exception as e:
            logging.warning(f"连接时发生错误: {e}")
            self.window.evaluate_js("ButtonState('connect_device',true,'连接')")

    def disconnected_callback(self, client):
        logging.info("Disconnected callback called!")
        self.disconnect_event.clear()

    async def enable_heart_rate_notifications(self):
        """启用心率通知"""

        def heart_rate_handler(sender, data):
            # 解析心率数据（根据BLE规范）
            flags = data[0]
            self.heart_rate = int.from_bytes(data[1:3], 'little') if flags & 0x01 else data[1]

            #

            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - 心率: {self.heart_rate} bpm")
            self.server.set_rate(self.heart_rate)

        # 查找心率特征值
        services = self.client.services
        self.heart_rate_char = services.get_characteristic(HEART_RATE_SERVICE_UUID)

        if self.heart_rate_char:
            await self.client.start_notify(self.heart_rate_char, heart_rate_handler)
            await self.disconnect_event.wait()
        else:
            logging.warning("未找到心率服务")

    def disconnect_device(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.disconnect())
            loop.run_until_complete(asyncio.sleep(0.1))  # 给事件处理一点时间
        finally:
            loop.close()

    async def disconnect(self):
        """改进版断开连接方法"""
        logging.info(f'开始断开蓝牙连接流程...{self.client.address if self.client else "无客户端"}')

        if self.client and self.client.is_connected:
            try:
                self.window.evaluate_js("ButtonState('disconnect_device',false,'断开中...')")
                # 停止心率通知
                if self.heart_rate_char:
                    try:
                        logging.info('正在停止心率通知...')
                        await asyncio.wait_for(
                            self.client.stop_notify(self.heart_rate_char),
                            timeout=3.0
                        )
                        logging.info('已停止心率通知')
                        self.heart_rate_char = None
                    except asyncio.TimeoutError:
                        logging.warning('停止心率通知超时')
                    except Exception as e:
                        logging.warning(f"停止心率通知时发生错误: {e}")

                self.disconnect_event.set()
                await asyncio.sleep(0.1)

                # 主动断开连接
                try:
                    logging.info('正在断开蓝牙连接...')
                    await asyncio.wait_for(self.client.disconnect(), timeout=5)
                    logging.info('已成功断开蓝牙连接')
                except asyncio.TimeoutError:
                    logging.warning('断开连接超时，尝试强制清理')
                    await self.force_disconnect()
                except Exception as e:
                    logging.warning(f"断开蓝牙连接时发生错误: {e}")
                    await self.force_disconnect()
            finally:
                self.client = None
                self.window.evaluate_js("ButtonState('disconnect_device',true,'断开')")
                self.window.evaluate_js("ListState(true)")
                self.window.evaluate_js("ButtonState('connect_device',true,'连接')")
                self.window.evaluate_js("startHeartRate(false)")
        else:
            logging.info("未建立有效连接，无需断开")
            await self.force_disconnect()

    async def force_disconnect(self):
        """强制断开连接并清理资源"""
        if self.client:
            try:
                # 尝试获取底层传输并关闭
                if hasattr(self.client, '_client'):
                    client_impl = self.client._client
                    if hasattr(client_impl, '_transport'):
                        try:
                            client_impl._transport.close()
                            logging.debug("已关闭传输层")
                        except Exception as e:
                            logging.debug(f"关闭传输层时发生错误: {e}")
            finally:
                pass


if __name__ == '__main__':
    print("蓝牙设备搜索中...")
    asyncio.run(Device_handle().scan_devices())
