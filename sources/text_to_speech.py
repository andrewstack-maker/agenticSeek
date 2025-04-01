import re
import platform
import subprocess
from sys import modules
from typing import List, Tuple, Type, Dict, Tuple

from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf

class Speech():
    """
    Speech is a class for generating speech from text.
    """
    def __init__(self, enable: bool = True, language: str = "en", voice_idx: int = 0) -> None:
        self.lang_map = {
            "en": 'a',
            "zh": 'z',
            "fr": 'f'
        }
        self.voice_map = {
            "en": ['af_kore', 'af_bella', 'af_alloy', 'af_nicole', 'af_nova', 'af_sky', 'am_echo', 'am_michael', 'am_puck'],
            "zh": ['zf_xiaobei', 'zf_xiaoni', 'zf_xiaoxiao', 'zf_xiaoyi', 'zm_yunjian', 'zm_yunxi', 'zm_yunxia', 'zm_yunyang'],
            "fr": ['ff_siwis']
        }
        self.pipeline = None
        self.language = language
        if enable:
            self.pipeline = KPipeline(lang_code=self.lang_map[language])
        self.voice = self.voice_map[language][voice_idx]
        self.speed = 1.2

    def speak(self, sentence: str, voice_number: int = 1 , audio_file: str = 'sample.wav'):
        """
        Convert text to speech using an AI model and play the audio.

        Args:
            sentence (str): The text to convert to speech. Will be pre-processed.
            voice_number (int, optional): Index of the voice to use from the voice map.
        """
        if not self.pipeline:
            return
        sentence = self.clean_sentence(sentence)
        self.voice = self.voice_map[self.language][voice_number]
        generator = self.pipeline(
            sentence, voice=self.voice,
            speed=self.speed, split_pattern=r'\n+'
        )
        for i, (_, _, audio) in enumerate(generator):
            if 'ipykernel' in modules: #only display in jupyter notebook.
                display(Audio(data=audio, rate=24000, autoplay=i==0), display_id=False)
            sf.write(audio_file, audio, 24000) # save each audio file
            if platform.system().lower() == "windows":
                import winsound
                winsound.PlaySound(audio_file, winsound.SND_FILENAME)
            elif platform.system().lower() == "darwin":  # macOS
                subprocess.call(["afplay", audio_file])
            else: # linux or other.
                subprocess.call(["aplay", audio_file])

    def replace_url(self, url: re.Match) -> str:
        """
        Replace URL with domain name or empty string if IP address.
        Args:
            url (re.Match): Match object containing the URL pattern match
        Returns:
            str: The domain name from the URL, or empty string if IP address
        """
        domain = url.group(1)
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            return ''
        return domain

    def extract_filename(self, m: re.Match) -> str:
        """
        Extract filename from path.
        Args:
            m (re.Match): Match object containing the path pattern match
        Returns:
            str: The filename from the path
        """
        path = m.group()
        parts = re.split(r'/|\\', path)
        return parts[-1] if parts else path
    
    def shorten_paragraph(self, sentence):
        #TODO find a better way, we would like to have the TTS not be annoying, speak only useful informations
        """
        Find long paragraph like **explaination**: <long text> by keeping only the first sentence.
        Args:
            sentence (str): The sentence to shorten
        Returns:
            str: The shortened sentence
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
        Clean and normalize text for speech synthesis by removing technical elements.
        Args:
            sentence (str): The input text to clean
        Returns:
            str: The cleaned text with URLs replaced by domain names, code blocks removed, etc..
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
