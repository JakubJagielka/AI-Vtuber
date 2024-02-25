import json
from openai import OpenAI

def prev_content( nickname):
    # Check if the nickname already exists in the "users" list
    json_data = json.load(open('files/conversations_logs.json'))
    user_found = False
    for user in json_data['users']:
        if user['nickname'] == nickname:
            # Nickname found, append the message
            user_found = True
            return user['messages'], user['responses'], user['user_content']
    # If the nickname is not found, add a new user with the given nickname and message
    if not user_found:
        return [], [], []

def save_response(nickname, message, response):
    json_data = json.load(open('files/conversations_logs.json'))
    user_found = False

    for user_entry in json_data['users']:
        if user_entry['nickname'] == nickname:
            # Nickname found, append the message
            user_found = True
            user_entry['responses'].append(response)
            user_entry['messages'].append(message)
            break

    # If the nickname is not found, add a new user with the given nickname and message
    if not user_found:
        new_user = {
            "nickname": nickname,
            "messages": [message],
            "responses": [response],
            "user_content": []
        }
        json_data['users'].append(new_user)

    # Convert the updated JSON structure back to a string
    updated_json_string = json.dumps(json_data, indent=2)
    with open('files/conversations_logs.json', 'w') as f:
        f.write(updated_json_string)

def simplyfay_data():
    json_data = json.load(open('files/conversations_logs.json'))
    for user_entry in json_data['users']:
        if len(user_entry['messages']) > 11:
            user_entry['user_content'].append(shorten_data(''.join(user_entry['messages'][:8])))
            user_entry['messages'] = user_entry['messages'][8:]
            user_entry['responses'] = user_entry['responses'][8:]
        updated_json_string = json.dumps(json_data, indent=2)
        with open('files/conversations_logs.json', 'w') as f:
            f.write(updated_json_string)


def shorten_data(mess):
    #openai api key
    clientai = OpenAI(api_key='')
    response = clientai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are making summary of user inputs. Try to get short information about him without too much assumptions, what he likes, personal information. It should skip the general and unrelevant information. The summary should be realativly short, few or more words (max 15 words), it will be used in future conversations with this user."},
            {"role": "user", "content": mess}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

