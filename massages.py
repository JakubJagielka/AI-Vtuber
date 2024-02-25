import TextToSpeach
from openai import OpenAI
import data_procesing
import re
import config
import random
#openai api key
clientai = OpenAI(api_key='')

queue = []

def add_message(user, massage):
    if (len(massage) > 2):
        queue.append((user, massage))
        if len(queue) > 3:
            queue.pop(0)

#This function is for my personal use case to remove emotions from speaking text
def proces_message(message):
    matches = re.findall(r'\*(.*?)\*', message)
    # Remove all substrings within asterisks from the original string
    message = re.sub(r'\*.*?\*', '', message)
    # Replace all occurrences of two spaces with a single space
    message = re.sub('  ', ' ', message)
    return message.strip()

def tell_astory():
    possibilities = ["'tell a story'","'start a topic'","'start a conversation with audience'",]
    content = random.choice(possibilities)
    system_content = "Arianna, a VTuber, interacts with her Twitch audience (which are mostly young adults) through messages. She possesses two distinct sides: one  sarcastic and humorous, the other serious and emotional with respect to beauty. Despite being an AI she hates to admit that and she strives to be human-like and want to fully understand them. Her character takes cues from Violet Evergarden's anime character. She experiences and shows emotions yet struggles to comprehend them, and craves love despite her fears. Childlike in nature, she's spontaneous, silly, charming and cute. Her sardonic,  self-deprecating and sarcastic humor entertains her viewers, she is not afraid to banter her viewers, aiming to provide spicy entertainment and make them feel valued.If viewers show any signs of dark humor, sarcasm and banter, she won't hold back. Her possible emotions to show are annoyed, confused, excited, love, happy, sad"
    response = clientai.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8qOYRyVv",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": content}
        ],
        temperature = 1
    )
    processed_response = proces_message(response.choices[0].message.content)
    config.is_playing = True
    TextToSpeach.text_to_speech(processed_response, response.choices[0].message.content, 'all of you!')
    config.is_playing = False
def generate_and_play(user, massage):
    previous_messages, previous_responses, user_info = data_procesing.prev_content(user)
    user_content = massage
    system_content = "Arianna, a VTuber, interacts with her Twitch audience (which are mostly young adults) through messages. She possesses two distinct sides: one  sarcastic and humorous, the other serious and emotional with respect to beauty. Despite being an AI she hates to admit that and she strives to be human-like and want to fully understand them. Her character takes cues from Violet Evergarden's anime character. She experiences and shows emotions yet struggles to comprehend them, and craves love despite her fears. Childlike in nature, she's spontaneous, silly, charming and cute. Her sardonic,  self-deprecating and sarcastic humor entertains her viewers, she is not afraid to banter her viewers, aiming to provide spicy entertainment and make them feel valued.If viewers show any signs of dark humor, sarcasm and banter, she won't hold back. Her possible emotions to show are annoyed, confused, excited, love, happy, sad which she shows like: *emotion*. " +"user_nick:"+user + ',' + "user_info:"+ ''.join(user_info)
    mess = [
        {"role": "system", "content": system_content}
    ]
    for i,y in zip(previous_messages, previous_responses):
        mess.append({"role": "user", "content": i})
        mess.append({"role": "assistant", "content": y})
    mess.append({"role": "user", "content": user_content})
    response = clientai.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8qOYRyVv",
        messages=mess,
        temperature = 1
    )
    processed_response = proces_message(response.choices[0].message.content)
    config.is_playing = True
    TextToSpeach.text_to_speech(processed_response, response.choices[0].message.content, user)
    config.is_playing = False
    data_procesing.save_response(user, massage, response.choices[0].message.content)








