import json
import threading

from bleak import BleakScanner, BleakClient
import asyncio


class Device_handle:
    """
    This class is used to handle the device.
    """

    def __init__(self):
        self.heart_rate_char = None
        self.client = None
        self.heart_rate = None
        self.ble_devices = []
        self._set_device = None
        self.window = None

        self.disconnect_event = asyncio.Event()

        # thread
        self.scan_thread = None
        self.connect_thread = None
        self.disconnect_thread = None

    def init(self, window):
        self.window = window
        self.window.expose(self.refresh_devices, self.set_device, self.connect_device, self.disconnect_device)

    async def scan_ble_devices(self):
        """
        扫描附近的蓝牙低功耗(BLE)设备，并返回发现的设备列表。

        Returns:
            list: 包含发现的BLE设备的列表，每个设备是一个BleakDevice对象。
        """
        try:
            print("蓝牙设备搜索中...")
            devices = await BleakScanner.discover()

            if not devices:
                print("未发现任何蓝牙设备。")
                return []

            named_devices = []
            for device in devices:
                if device.name is not None:
                    named_devices.append(device)
                    print(f"Address: {device.address}, Name: {device.name}")

            if not named_devices:
                print("未发现任何有名称的蓝牙设备。")
                return []

            return named_devices
        except Exception as e:
            print(f"扫描 BLE 设备时发生错误: {e}")
            return []

    def refresh_device(self):
        """
        搜索蓝牙设备。
        """
        try:
            if self.scan_thread:
                print("[INFO] 已经运行")
                return
            self.scan_thread = True
            self.ble_devices = []
            self.ble_devices = asyncio.run(self.scan_ble_devices())
            self.scan_thread = False

            # 构造可序列化的设备列表
            devices_data = [
                {"name": device.name, "address": device.address}
                for device in self.ble_devices
            ]

            # 使用 json.dumps 确保 JS 可以正确解析
            js_code = f"update_devices({json.dumps(devices_data)})"
            self.window.evaluate_js(js_code)
            self._set_device = None
        except Exception as e:
            print(f"搜索蓝牙设备时发生错误: {e}")

    def refresh_devices(self):
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
        """
        设置蓝牙设备。
        """
        self._set_device = device
        print(device)

    def connect_device(self):
        """
        连接蓝牙设备。
        """
        if self.client:
            print(f"[INFO] 设备 {self._set_device['name']} 已经连接。")
            return
        if self._set_device:
            print(f"正在连接蓝牙设备: {self._set_device['name']}")
            try:
                self.connect_thread = threading.Thread(target=self.run_async_connect, daemon=True)
                self.connect_thread.start()
                print(f"已连接蓝牙设备: {self._set_device['name']}")
            except Exception as e:
                print(f"连接蓝牙设备时发生错误: {e}")
        else:
            print("请选择要连接的蓝牙设备。")

    def run_async_connect(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.connect())
        finally:
            loop.close()

    async def connect(self):
        address = self._set_device['address']
        client = BleakClient(address)
        if client.is_connected:
            print(f"设备 {address} 已经连接。")
            return
        await client.connect()
        if client.is_connected:
            self.client = client
            print(f"成功连接到设备: {address}")

            print(f"通讯连接成功: {client.address}")
            # 查找心率特征值
            # servers = await client.get_services()
            services = client.services
            # 心率测量特征UUID
            HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
            self.heart_rate_char = services.get_characteristic(HEART_RATE_MEASUREMENT_UUID)
            # 订阅心率测量特征值
            if self.heart_rate_char is None:
                print(f"未找到心率测量特征值")
                return
            await self.client.start_notify(self.heart_rate_char,
                                           lambda sender, data: self.notification_handler(sender, data))
            print("开始接收心率数据...")
            # 保持连接一段时间以接收数据
            # await input_key(disconnect_event)
            # await asyncio.sleep(9999)
            await self.disconnect_event.wait()
        else:
            print(f"无法连接到设备: {address}")

    def notification_handler(self, sender, data):
        """
        处理接收到的心率数据。
        """
        try:
            # 校验数据格式
            flags = data[0]
            if flags & 0x01:
                heart_rate = int.from_bytes(data[1:3], byteorder='little')
            else:
                heart_rate = data[1]
            print(f"接收到的心率数据: {heart_rate} BPM")
            self.heart_rate = heart_rate
        except Exception as e:
            print(f"处理心率数据时发生错误: {e}")

    def disconnect_device(self):
        """
        断开蓝牙连接。
        """
        if self.disconnect_thread and self.disconnect_thread.is_alive():
            print("[INFO] 已经运行")
            return
        if not self.client or not self.client.is_connected:
            print("未连接到任何蓝牙设备。")
            return
        try:
            self.disconnect_thread = threading.Thread(target=self.run_async_disconnect, daemon=True)
            self.disconnect_thread.start()
        except Exception as e:
            print(f"断开蓝牙连接时发生错误: {e}")
            return

    def run_async_disconnect(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.disconnect())
        finally:
            loop.close()

    async def disconnect(self):
        print(f"正在断开蓝牙连接: {self.client.address}")
        self.disconnect_event.set()
        self.disconnect_event.clear()
        # print("停止接收心率数据...")
        # await self.client.stop_notify(self.heart_rate_char)

        await self.client.disconnect()
        print("蓝牙连接已断开")
        self.connect_thread.join()
        print(f"蓝牙连接已断开: {self.client.address}")
        self.client = None

        # self.disconnect_thread.join()
        # self.disconnect_thread = None


if __name__ == '__main__':
    print("蓝牙设备搜索中...")
    asyncio.run(Device_handle().scan_ble_devices())
