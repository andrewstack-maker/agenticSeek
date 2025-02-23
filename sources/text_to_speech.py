from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import subprocess
import re

class Speech():
    def __init__(self, language = "english") -> None:
        self.lang_map = {
            "english": 'a',
            "chinese": 'z',
            "french": 'f'
        }
        self.voice_map = {
            "english": ['af_alloy', 'af_aoede', 'af_bella', 'af_heart', 'af_jessica', 'af_kore', 'af_nicole', 'af_nova', 'af_river', 'af_sarah', 'af_sky', 'am_adam', 'am_echo', 'am_eric', 'am_fenrir', 'am_liam', 'am_michael', 'am_onyx', 'am_puck'],
            "chinese": ['zf_xiaobei', 'zf_xiaoni', 'zf_xiaoxiao', 'zf_xiaoyi', 'zm_yunjian', 'zm_yunxi', 'zm_yunxia', 'zm_yunyang'],
            "french": ['ff_siwis']
        }
        self.pipeline = KPipeline(lang_code=self.lang_map[language])
        self.voice = self.voice_map[language][0]

    def speak(self, sentence):
        sentence = self.clean_sentence(sentence)
        generator = self.pipeline(
            sentence, voice=self.voice,
            speed=1, split_pattern=r'\n+'
        )
        for i, (gs, ps, audio) in enumerate(generator):
            audio_file = f'sample.wav'
            display(Audio(data=audio, rate=24000, autoplay=i==0))
            sf.write(audio_file, audio, 24000) # save each audio file
            subprocess.call(["afplay", audio_file])
    
    def clean_sentence(self, sentence):
        sentence = re.sub(r'`.*?`', '', sentence)
        sentence = re.sub(r'[^a-zA-Z0-9.,!? ]+', '', sentence)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        return sentence

if __name__ == "__main__":
    speech = Speech()
    speech.speak("hello would you like coffee ?")
