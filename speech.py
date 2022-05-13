import speech_recognition as sr  # SpeechRecognition 3.8.1
import threading
from datetime import datetime


# -----------------------------------------------------------------------
def getAudioFromURL(URL):
    from urllib.request import urlopen

    data = urlopen(URL).read()
    return data


# -----------------------------------------------------------------------
def getTextFromVoice(audioData):  # распознавание голоса
    import tempfile
    from pydub import AudioSegment  # для работы требуется ffmpeg

    with tempfile.NamedTemporaryFile() as temp_ogg:
        with tempfile.NamedTemporaryFile() as temp_wav:
            temp_ogg.write(audioData)
            temp_ogg.seek(0)
            try:
                AudioSegment.from_file_using_temporary_files(temp_ogg, 'ogg').export(temp_wav, format='wav')
            except FileNotFoundError as e:
                print("Установите и проверьте работоспособность библиотеки ffmpeg!")
                return "Установите и проверьте работоспособность библиотеки ffmpeg!"

            r = sr.Recognizer()
            # with sr.Microphone(device_index=2) as source:
            with sr.AudioFile(temp_wav) as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    query = r.recognize_google(audio, language='ru-RU').lower()
                    return query
                except Exception as e:
                    return "Ошибка распознавания:\n" + str(e)


