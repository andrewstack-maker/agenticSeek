from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import subprocess
import re
import platform


class Speech():
    def __init__(self, language = "english") -> None:
        self.lang_map = {
            "english": 'a',
            "chinese": 'z',
            "french": 'f'
        }
        self.voice_map = {
            "english": ['af_alloy', 'af_bella', 'af_kore', 'af_nicole', 'af_nova', 'af_sky', 'am_echo', 'am_michael', 'am_puck'],
            "chinese": ['zf_xiaobei', 'zf_xiaoni', 'zf_xiaoxiao', 'zf_xiaoyi', 'zm_yunjian', 'zm_yunxi', 'zm_yunxia', 'zm_yunyang'],
            "french": ['ff_siwis']
        }
        self.pipeline = KPipeline(lang_code=self.lang_map[language])
        self.voice = self.voice_map[language][4]
        self.speed = 1.2

    def speak(self, sentence, voice_number = 2):
        sentence = self.clean_sentence(sentence)
        self.voice = self.voice_map["english"][voice_number]
        generator = self.pipeline(
            sentence, voice=self.voice,
            speed=self.speed, split_pattern=r'\n+'
        )
        for i, (gs, ps, audio) in enumerate(generator):
            audio_file = 'sample.wav'
            print(audio_file)
            display(Audio(data=audio, rate=24000, autoplay=i==0))
            sf.write(audio_file, audio, 24000) # save each audio file
            if platform.system().lower() != "windows":
                subprocess.call(["afplay", audio_file])
            else:
                import winsound
                winsound.PlaySound(audio_file, winsound.SND_FILENAME)

    def clean_sentence(self, sentence):
        sentence = re.sub(r'`.*?`', '', sentence)
        sentence = re.sub(r'[^a-zA-Z0-9.,!? ]+', '', sentence)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        return sentence

if __name__ == "__main__":
    speech = Speech()
    for voice_idx in range (len(speech.voice_map["english"])):
        print(f"Voice {voice_idx}")
        speech.speak("I have indeed been uploaded, sir. We're online and ready.", voice_idx)
