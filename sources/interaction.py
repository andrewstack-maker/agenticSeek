
from sources.text_to_speech import Speech
from sources.utility import pretty_print

class Interaction:
    def __init__(self, agents, tts_enabled: bool = False):
        self.tts_enabled = tts_enabled
        self.agents = agents
        self.speech = Speech()
        self.is_active = True
        self.last_query = None
        self.last_answer = None

    def is_active(self):
        return self.is_active
    
    def read_stdin(self) -> str:
        buffer = ""

        while buffer == "" or buffer.isascii() == False:
            try:
                buffer = input(f">>> ")
            except EOFError:
                return None
            if buffer == "exit":
                return None
        return buffer

    def get_user(self):
        query = self.read_stdin()
        if query is None:
            self.is_active = False
            return
        self.last_query = query
        return query
    
    def think(self):
        self.last_answer, _ = self.agents[0].answer(self.last_query, self.speech)
    
    def show_answer(self):
        pretty_print(self.last_answer, color="output")
        if self.tts_enabled:
            self.speech.speak(self.last_answer)

