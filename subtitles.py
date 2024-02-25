import time
import obsws_python as obs
import re
cl = obs.ReqClient(host='localhost', port=4445)
punctuation = ['.', '!', '?',',']

#this subtitle function connects to obs text element and displays subtitles on the screen in real time
def main():
    while True:
        time.sleep(1)
        with open('files/odpowiedz.txt', 'r') as f:
            data = f.read()
        with open('filles/user_nick.txt', 'r') as f:
            nick = f.read()
        if data == '':
            continue
        else:
            with open('files/odpowiedz.txt', 'w') as f:
                pass
            with open('files/user_nick.txt', 'w') as f:
                pass
            try:
                data = re.sub(r'\*+', '*', data)
                print(data)
                subtitles = ''
                inemotion = False
                charpertime = 0.064
                cl.set_input_settings('Respondingto', {'text': 'Responding to: ' + nick}, overlay=True)
                i = 0
                while i < len(data):
                    if data[i] == '*':
                        i += 1
                        emotion = ''
                        print(data[i])
                        while data[i] != '*':
                            emotion += data[i]
                            i += 1
                        i += 1
                        with open('files/emotion.txt', 'w', encoding='utf-8') as f:
                            f.write(str(emotion))
                    else:
                        subtitles += data[i]
                        cl.set_input_settings('Tekstnew3', {'text': subtitles}, overlay=True)
                        time.sleep(charpertime)
                        if data[i] in punctuation:
                            if i < len(data) - 1 and data[i+1] in punctuation:
                                while data[i] in punctuation:
                                    if i< len(data)-1:
                                        i += 1
                                        subtitles += data[i]
                                        cl.set_input_settings('Tekstnew3', {'text': subtitles}, overlay=True)
                                    else:
                                        time.sleep(0.40)
                                        break

                            time.sleep(0.40)
                            subtitles = ''
                            if data[i] == '*':
                                continue
                        i += 1

                time.sleep(1)

            except:
                pass
            finally:
                cl.set_input_settings('Tekstnew3', {'text': ''}, overlay=True)
                cl.set_input_settings('Respondingto', {'text': ''}, overlay=True)

