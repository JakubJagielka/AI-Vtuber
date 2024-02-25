# AI-Vtuber
Python-only application which allows you to stream AI VTuber.

# Important
This repo was not created as a copy-and-paste application, but more of an inspiration for how to approach a project like this. It was created to fit my personal case; it's not universal.

# How it works
It uses the Twitch API to read messages from chat. It checks if the user has previous content and then OpenAI fine-tuned GPT-3.5 Turbo model processes it. The response is then saved to a file and played using the ElevenLabs API. The audio is streamed, captured, and subtitles are played in the meantime. It communicates with VTube Studio and OBS.

# Example
You can see how it can look in the example below.

https://clips.twitch.tv/FastPlayfulGrasshopperMrDestructoid-h4inCzz8Ig1Ac2V0
