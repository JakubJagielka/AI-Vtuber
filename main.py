from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
import massages
import asyncio
import multiprocessing
import data_procesing
import vtuber
import config
import subtitles
import time
import os
#creditalials for twitch
APP_ID = ''
APP_SECRET = ''
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT,AuthScope.MODERATOR_READ_CHATTERS]
TARGET_CHANNEL = ''

chars = ['!', '@', '#', ',']

def run_vtuber():
    asyncio.run(vtuber.run_vtuber())

#function to check how many people are in the chat(not working too well)
async def get_total_chatters():
    chatters = await twitch.get_chatters('your id', 'your id')
    v = vars(chatters)
    return v['total']

async def runing():
    data_procesing.simplyfay_data()
    last_simplyfay = time.time()
    last_story = time.time()
    while 1:
        if len(massages.queue) > 0: #triger to play a message if somebody wrote something
            if config.is_playing is False:
                massages.generate_and_play(massages.queue[0][0], massages.queue[0][1])
                massages.queue.pop(0)
                last_story += 15
        elif time.time() - last_simplyfay > 500: #triger to simplyfay data in json to shorten a long conversation every 500 seconds
            last_simplyfay = time.time()
            data_procesing.simplyfay_data()
        elif  time.time() - last_story > 120: # trigger to telling a story every 120 seconds
            last_story = time.time()
            try:
                l = await asyncio.create_task(get_total_chatters())
                if l > 19:
                    massages.tell_astory()
            except:
                pass

# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    if msg.text.strip()[0] not in chars:
        print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
        massages.add_message(msg.user.name, msg.text)
    elif msg.text.strip()[0] == '!':
        with open('files/tools.txt', 'w', encoding='utf-8') as f:
            f.write(str(msg.text[1:].replace(' ', '')))


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    global twitch
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # there are more events, you can view them all in this documentation
    # we are done with our setup, lets start this bot up!
    chat.start()

    await asyncio.create_task(runing())


def start():
    asyncio.run(run())



if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    p1 = multiprocessing.Process(target=run_vtuber)
    p2 = multiprocessing.Process(target=start)
    p3 = multiprocessing.Process(target=subtitles.main) # subtitles are optional
    p1.start()
    p2.start()
    p3.start()






