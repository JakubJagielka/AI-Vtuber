import pyvts
import asyncio
import aiofiles
import time

#In this file i make changes to vtube sutdio model  by the api, i toggle hotkeys that i set before.
class Vtuber:
    def __init__(self, myvts):
        self.myvts = myvts
        self.current_emotion = ' '
        self.toggled = []

    async def connect(self):
        await self.myvts.connect()
        await self.myvts.request_authenticate_token()
        await self.myvts.request_authenticate()

    async def dostaff(self):
        await asyncio.sleep(1)
        async with aiofiles.open('files/emotion.txt', mode='r') as f:
            emotion = await f.read()
        if emotion != self.current_emotion:
            self.current_emotion = emotion
            await self.set_emotion(emotion)
        async with aiofiles.open('files/tools.txt', mode='a+') as t:
            await t.seek(0)
            toogle = await t.read()
            async with aiofiles.open('files/tools.txt', mode='w') as f:
                pass
        if toogle != '' and  toogle not in [toggle for toggle, _ in self.toggled]:
            self.toggled.append([toogle, time.time()])
            await self.set_emotion(toogle)

    async def time_staff(self):
        await asyncio.sleep(1)  # check every 5 seconds
        current_time = time.time()
        self.toggled = [[toggle, timestamp] for toggle, timestamp in self.toggled if current_time - timestamp <= 1]

    async def run(self):
        await self.connect()
        while True:
            await self.dostaff()
            await self.time_staff()
    async def set_emotion(self, emotion):
        await self.myvts.request(self.myvts.vts_request.requestTriggerHotKey(emotion))


def run_vtuber():
    my_vtuber = Vtuber(pyvts.vts())
    try:
        asyncio.run(my_vtuber.run())
    except Exception as e:
        print(f"Exception in run_vtuber: {e}")


