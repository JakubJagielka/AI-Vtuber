from elevenlabs import generate, set_api_key
import subprocess
from typing import Iterator

#elevenlabs api key
set_api_key('')

znaki = [',','.','!','?',' ']

def stream(audio_stream: Iterator[bytes],text, user_nick) -> bytes:
    global pierwszy
    mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
    mpv_process = subprocess.Popen(
        mpv_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    audio = b""

    for chunk in audio_stream:
        #sending the data  to the subtitles when the audio starts playing
        if pierwszy:
            with open('files/odpowiedz.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            with open('files/user_nick.txt', 'w', encoding='utf-8') as f:
                f.write(user_nick)
            pierwszy = False
        if chunk is not None:
            mpv_process.stdin.write(chunk)  # type: ignore
            mpv_process.stdin.flush()  # type: ignore
            audio += chunk

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()
    return audio




def text_to_speech(text, text_subt, user_nick):
    global pierwszy
    audio_stream = generate(
        text=text,
        model='eleven_turbo_v2',
        output_format="mp3_44100_128",
        voice='Ella - soft and sweet',
        stream=True,
        stream_chunk_size = 2048,
        latency=3
    )
    pierwszy = True
    stream(audio_stream,text_subt, user_nick)

    return False
