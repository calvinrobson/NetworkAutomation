import asyncio
import netdev
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)

async def task(param):
    async with netdev.create(**param) as ios:
        # Testing sending simple command
        out = await ios.send_command("show ip int br")
        print(out)
       

async def run():
    dev1 = { 'username' : 'calvin',
             'password' : 'password',
             'secret': 'password',
             'device_type': 'cisco_ios',
             'host': '192.168.16.131',
    }
    devices = [dev1]
    tasks = [task(dev) for dev in devices]
    await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())