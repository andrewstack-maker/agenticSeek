from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import subprocess
import re
import platform

class Speech():
    """
    Speech is a class for generating speech from text.
    """
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
        self.voice = self.voice_map[language][2]
        self.speed = 1.2

    def speak(self, sentence, voice_number = 1):
        """
        Use AI model to generate speech from text after pre-processing the text.
        """
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

    def replace_url(self, m):
        """
        Replace URL with empty string.
        """
        domain = m.group(1)
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            return ''
        return domain

    def extract_filename(self, m):
        """
        Extract filename from path.
        """
        path = m.group()
        parts = re.split(r'/|\\', path)
        return parts[-1] if parts else path
    
    def shorten_paragraph(self, sentence):
        """
        Shorten paragraph like **explaination**: <long text> by keeping only the first sentence.
        """
        lines = sentence.split('\n')
        lines_edited = []
        for line in lines:
            if line.startswith('**'):
                lines_edited.append(line.split('.')[0])
            else:
                lines_edited.append(line)
        return '\n'.join(lines_edited)

    def clean_sentence(self, sentence):
        """
        Clean sentence by removing URLs, filenames, and other non-alphanumeric characters.
        """
        lines = sentence.split('\n')
        filtered_lines = [line for line in lines if re.match(r'^\s*[a-zA-Z]', line)]
        sentence = ' '.join(filtered_lines)
        sentence = re.sub(r'`.*?`', '', sentence)
        sentence = re.sub(r'https?://(?:www\.)?([^\s/]+)(?:/[^\s]*)?', self.replace_url, sentence)
        sentence = re.sub(r'\b[\w./\\-]+\b', self.extract_filename, sentence)
        sentence = re.sub(r'\b-\w+\b', '', sentence)
        sentence = re.sub(r'[^a-zA-Z0-9.,!? _ -]+', ' ', sentence)
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        sentence = sentence.replace('.com', '')
        return sentence

if __name__ == "__main__":
    speech = Speech()
    tosay = """
    I looked up recent news using the website https://www.theguardian.com/world
    Here is how to list files:
    ls -l -a -h
    the ip address of the server is 192.168.1.1
    """
    for voice_idx in range (len(speech.voice_map["english"])):
        print(f"Voice {voice_idx}")
        speech.speak(tosay, voice_idx)
