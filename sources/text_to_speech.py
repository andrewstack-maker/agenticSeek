from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import subprocess
import re

class Speech():
    def __init__(self, language = "english") -> None:
        self.lang_map = {
            "english": 'a', # 🇺🇸 'a' => American English 
            "chinese": 'z', # 🇯🇵 'j' => Japanese: pip install misaki[ja]
            "japanese": 'j' # # 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]
        }
        self.pipeline = KPipeline(lang_code=self.lang_map[language])

    def speak(self, sentence):
        sentence = self.clean_sentence(sentence)
        generator = self.pipeline(
            sentence, voice='af_heart', # <= change voice here
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
