import asyncio
from bleak import BleakScanner

async def scan_for_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")

# Run the scan once
asyncio.run(scan_for_devices())

#Device: Mikey’s iPhone, Address: A049F3D3-7556-C22D-495B-3FA8211AB2F9