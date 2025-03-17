from flask import Flask, jsonify, request
import threading
import ollama
import logging
import json

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Shared state with thread-safe locks
class Config:
    def __init__(self):
        self.model = None
        self.known_models = []
        self.allowed_models = []
        self.model_name = None

    def load(self):
        with open('config.json', 'r') as f:
            data = json.load(f)
            self.known_models = data['known_models']
            self.model_name = data['model_name']

    def validate_model(self, model):
        if model not in self.known_models:
            raise ValueError(f"Model {model} is not known")

class GenerationState:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_complete_sentence = ""
        self.current_buffer = ""
        self.is_generating = False
        self.model = None

state = GenerationState()

def generate_response(history):  # Only takes history as an argument
    global state
    try:
        with state.lock:
            state.is_generating = True
            state.last_complete_sentence = ""
            state.current_buffer = ""

        stream = ollama.chat(
            model=state.model,  # Access state.model directly
            messages=history,
            stream=True,
        )
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            with state.lock:
                state.current_buffer += content
    except ollama.ResponseError as e:
        if e.status_code == 404:
            ollama.pull(state.model)
        with state.lock:
            state.is_generating = False
        print(f"Error: {e}")
    finally:
        with state.lock:
            state.is_generating = False

@app.route('/generate', methods=['POST'])
def start_generation():
    global state
    data = request.get_json()

    with state.lock:
        if state.is_generating:
            return jsonify({"error": "Generation already in progress"}), 400

        history = data.get('messages', [])
        # Pass only history to the thread
        threading.Thread(target=generate_response, args=(history,)).start()  # Note the comma to make it a single-element tuple
    return jsonify({"message": "Generation started"}), 202

@app.route('/get_updated_sentence')
def get_updated_sentence():
    global state
    with state.lock:
        return jsonify({
            "sentence": state.current_buffer,
            "is_complete": not state.is_generating
        })

if __name__ == '__main__':
    config = Config()
    config.load()
    config.validate_model(config.model_name)
    state.model = config.model_name
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
