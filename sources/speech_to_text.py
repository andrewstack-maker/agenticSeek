from colorama import Fore
import pyaudio
import queue
import threading
import numpy as np
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import time
import librosa

audio_queue = queue.Queue()
done = False

class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=4096, chunk=8192, record_seconds=7, verbose=False):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.verbose = verbose
        self.audio = pyaudio.PyAudio()
        self.thread = threading.Thread(target=self._record, daemon=True)

    def _record(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate,
                                 input=True, frames_per_buffer=self.chunk)
        if self.verbose:
            print(Fore.GREEN + "AudioRecorder: Started recording..." + Fore.RESET)

        while not done:
            frames = []
            for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    print(Fore.RED + f"AudioRecorder: Failed to read stream - {e}" + Fore.RESET)
            
            raw_data = b''.join(frames)
            audio_data = np.frombuffer(raw_data, dtype=np.int16)
            audio_queue.put((audio_data, self.rate))
            if self.verbose:
                print(Fore.GREEN + "AudioRecorder: Added audio chunk to queue" + Fore.RESET)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        if self.verbose:
            print(Fore.GREEN + "AudioRecorder: Stopped" + Fore.RESET)

    def start(self):
        """Start the recording thread."""
        self.thread.start()

    def join(self):
        """Wait for the recording thread to finish."""
        self.thread.join()

class Transcript:
    def __init__(self) -> None:
        self.last_read = None
        device = self.get_device()
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        model_id = "distil-whisper/distil-medium.en"
        
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, use_safetensors=True
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)
        
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=24, # a human say around 20 token in 7s
            torch_dtype=torch_dtype,
            device=device,
        )
    
    def get_device(self):
        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda:0"
        else:
            return "cpu"
    
    def remove_hallucinations(self, text: str):
        # TODO find a better way to do this
        common_hallucinations = ['Okay.', 'Thank you.', 'Thank you for watching.', 'You\'re', 'Oh', 'you', 'Oh.', 'Uh', 'Oh,', 'Mh-hmm', 'Hmm.']
        for hallucination in common_hallucinations:
            text = text.replace(hallucination, "")
        return text
    
    def transcript_job(self, audio_data: np.ndarray, sample_rate: int = 16000):
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        if sample_rate != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
        result = self.pipe(audio_data)
        return self.remove_hallucinations(result["text"])

class AudioTranscriber:
    def __init__(self, ai_name: str, verbose=False):
        self.verbose = verbose
        self.ai_name = ai_name
        self.transcriptor = Transcript()
        self.thread = threading.Thread(target=self._transcribe, daemon=True)
        self.trigger_words = {
            'EN': [f"{self.ai_name}"],
            'FR': [f"{self.ai_name}"],
            'ZH': [f"{self.ai_name}"],
            'ES': [f"{self.ai_name}"]
        }
        self.confirmation_words = {
            'EN': ["do it", "go ahead", "execute", "run", "start", "thanks", "would ya", "please", "okay?", "proceed", "continue", "go on", "do that", "go it", "do you understand?"],
            'FR': ["fais-le", "vas-y", "exécute", "lance", "commence", "merci", "tu veux bien", "s'il te plaît", "d'accord ?", "poursuis", "continue", "vas-y", "fais ça", "compris"],
            'ZH': ["做吧", "继续", "执行", "运行", "开始", "谢谢", "可以吗", "请", "好吗", "进行", "继续", "往前走", "做那个", "做那件事", "聽得懂"],
            'ES': ["hazlo", "adelante", "ejecuta", "corre", "empieza", "gracias", "lo harías", "por favor", "¿vale?", "procede", "continúa", "sigue", "haz eso", "haz esa cosa"]
        }
        self.recorded = ""

    def get_transcript(self):
        global done
        buffer = self.recorded
        self.recorded = ""
        done = False
        return buffer

    def _transcribe(self):
        global done
        if self.verbose:
            print(Fore.BLUE + "AudioTranscriber: Started processing..." + Fore.RESET)
        
        while not done or not audio_queue.empty():
            try:
                audio_data, sample_rate = audio_queue.get(timeout=1.0)
                if self.verbose:
                    print(Fore.BLUE + "AudioTranscriber: Processing audio chunk" + Fore.RESET)
                
                text = self.transcriptor.transcript_job(audio_data, sample_rate)
                self.recorded += text
                print(Fore.YELLOW + f"Transcribed: {text}" + Fore.RESET)
                for language, words in self.trigger_words.items():
                    if any(word in text.lower() for word in words):
                        print(Fore.GREEN + f"Start listening..." + Fore.RESET)
                        self.recorded = text
                for language, words in self.confirmation_words.items():
                    if any(word in text.lower() for word in words):
                        print(Fore.GREEN + f"Trigger detected. Sending to AI..." + Fore.RESET)
                        audio_queue.task_done()
                        done = True
                        break
            except queue.Empty:
                time.sleep(0.1)
                continue
            except Exception as e:
                print(Fore.RED + f"AudioTranscriber: Error - {e}" + Fore.RESET)
        if self.verbose:
            print(Fore.BLUE + "AudioTranscriber: Stopped" + Fore.RESET)

    def start(self):
        """Start the transcription thread."""
        self.thread.start()

    def join(self):
        """Wait for the transcription thread to finish."""
        self.thread.join()


if __name__ == "__main__":
    recorder = AudioRecorder(verbose=True)
    transcriber = AudioTranscriber(verbose=True, ai_name="jarvis")
    recorder.start()
    transcriber.start()
    recorder.join()
    transcriber.join()