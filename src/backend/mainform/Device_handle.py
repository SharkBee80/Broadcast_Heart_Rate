import json
import time

from bleak import BleakScanner, BleakClient
import asyncio
from typing import Optional

from qasync import asyncSlot
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 心率服务UUID（标准特征值）
HEART_RATE_SERVICE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


class Device_handle:
    """
    This class is used to handle the device.
    """

    def __init__(self):
        self.window = None

        self._set_device = None
        self.client: Optional[BleakClient] = None
        self.heart_rate_char = None

        self.disconnect_event: Optional[asyncio.Event] = asyncio.Event()

    def init(self, window):
        self.window = window
        self.window.expose(self.refresh_devices, self.set_device, self.connect_device, self.disconnect_device)

    @asyncSlot()
    async def scan_devices(self):
        """开始扫描蓝牙设备"""
        try:
            logging.info("正在扫描蓝牙设备...")
            devices = await BleakScanner.discover()
            devices_data = []
            for d in devices:
                if d.name is not None:
                    device_data = {
                        'name': d.name,
                        'address': d.address
                    }
                    devices_data.append(device_data)
            print(f"发现 {len(devices_data)} 个设备")
            print(devices_data)
            js_code = f"update_devices({json.dumps(devices_data)})"
            self.window.evaluate_js(js_code)

        except Exception as e:
            logging.warning(f"扫描时发生错误: {e}")

    def refresh_devices(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.scan_devices())
            loop.run_until_complete(asyncio.sleep(0.1))  # 给事件处理一点时间
        finally:
            loop.close()

    def refresh_device(self):
        # 构造可序列化的设备列表
        devices_data = [
            {'name': 'iQOO WATCH 047', 'address': '88:54:8E:D9:50:47'},
            {'name': 'EDIFIER BLE', 'address': 'CC:14:BC:B5:14:C7'},
            {'name': 'AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGGHHHHH', 'address': 'AA:AA:AA:AA:AA:AA'}
        ]

        # 使用 json.dumps 确保 JS 可以正确解析
        js_code = f"update_devices({json.dumps(devices_data)})"
        self.window.evaluate_js(js_code)

    def set_device(self, device):
        self._set_device = device
        print(device)

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

    @asyncSlot()
    async def connect(self):
        """连接选定设备"""
        selected = self._set_device
        if not selected:
            logging.warning("未选择任何设备")
            return

        address = selected['address']
        logging.info(f"正在连接: {address}")

        try:
            self.client = BleakClient(address)
            await self.client.connect()

            if self.client.is_connected:
                logging.info(f"已连接: {address}")

                # 启用心率通知
                await self.enable_heart_rate_notifications()
            else:
                logging.warning(f"无法连接: {address}")

        except Exception as e:
            logging.warning(f"连接时发生错误: {e}")

    @asyncSlot()
    async def enable_heart_rate_notifications(self):
        """启用心率通知"""

        def heart_rate_handler(sender, data):
            # 解析心率数据（根据BLE规范）
            flags = data[0]
            heart_rate = int.from_bytes(data[1:3], 'little') if flags & 0x01 else data[1]

            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} - 心率: {heart_rate} bpm")

        # 查找心率特征值
        services = self.client.services
        heart_rate_char = services.get_characteristic(HEART_RATE_SERVICE_UUID)

        if heart_rate_char:
            await self.client.start_notify(heart_rate_char, heart_rate_handler)
            self.heart_rate_char = heart_rate_char
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

    @asyncSlot()
    async def disconnect(self):
        logging.info(f'正在断开蓝牙连接...{self.client.address}')
        """断开当前连接"""
        if self.client and self.client.is_connected:
            try:
                self.disconnect_event.set()
                if self.heart_rate_char:
                    # 设置最大等待时间为3秒
                    logging.info('正在停止心率通知...')
                    await self.client.stop_notify(self.heart_rate_char)
                    logging.info('已停止心率通知')
            except Exception as e:
                logging.warning(f"停止心率通知时发生错误: {e}")

            await asyncio.sleep(1)  # 或其他操作

            try:
                logging.info('正在断开蓝牙连接...')
                await self.client.disconnect()
                logging.info('已断开蓝牙连接')
            except Exception as e:
                logging.warning(f"断开蓝牙连接时发生错误: {e}")
            finally:
                print("心率: -- bpm")
        else:
            logging.info("未连接蓝牙设备")


if __name__ == '__main__':
    print("蓝牙设备搜索中...")
    asyncio.run(Device_handle().scan_devices())
