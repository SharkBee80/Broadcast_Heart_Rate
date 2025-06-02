import json

from bleak import BleakScanner
import asyncio


class Device_handle:
    """
    This class is used to handle the device.
    """

    def __init__(self):
        self.ble_devices = []
        self._set_device = None
        self.window = None

        # thread
        self.scan_thread = None

    def init(self, window):
        self.window = window
        self.window.expose(self.refresh_devices, self.set_device)

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
        except Exception as e:
            print(f"搜索蓝牙设备时发生错误: {e}")

        # 构造可序列化的设备列表
        devices_data = [
            {"name": device.name, "address": device.address}
            for device in self.ble_devices
        ]

        # 使用 json.dumps 确保 JS 可以正确解析
        js_code = f"update_devices({json.dumps(devices_data)})"
        self.window.evaluate_js(js_code)

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


if __name__ == '__main__':
    print("蓝牙设备搜索中...")
    asyncio.run(Device_handle().scan_ble_devices())
