import asyncio
from bleak import BleakClient

# Replace this with the device address you got from your scan
device_address = "A049F3D3-7556-C22D-495B-3FA8211AB2F9"

# Bluetooth service and characteristic UUIDs for heart rate
heart_rate_service_uuid = "0000180d-0000-1000-8000-00805f9b34fb"
heart_rate_characteristic_uuid = "00002a37-0000-1000-8000-00805f9b34fb"

async def monitor_heart_rate():
    async with BleakClient(device_address) as client:
        print("Connected to BlueHeart device.")
        
        while True:
            # Read heart rate data
            heart_rate_data = await client.read_gatt_char(heart_rate_characteristic_uuid)
            # Extract heart rate value from the byte data
            heart_rate = int.from_bytes(heart_rate_data[1:], byteorder="big")
            print(f"Heart rate: {heart_rate}")
            
            # Adjust interval if needed
            await asyncio.sleep(1)

# Run the monitor function
asyncio.run(monitor_heart_rate())
