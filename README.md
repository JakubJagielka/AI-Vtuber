# AI-Vtuber
Python only application which allows you to stream ai vtuber

#Important
This repo was not created as copy and paste application, but more of a inspiration of how to approach project like this.
It was created to fit my personal case, it's not universal.

#How it works
It uses Twitch API to read massages from chat, it checks if user has previous content and then openai fine-tuned gpt-3.5 turbo model processes it.
The response then is saved to file and then i play the response from ElevenLabs API. The audio is streamed and captured and subtitles are playing in the meantime.
It uses VTube Studio and OBS and communicate with it.
