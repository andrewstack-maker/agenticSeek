#!/usr/bin python3

from flask import Flask, jsonify, request
import threading
import ollama
import logging
import argparse

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

parser = argparse.ArgumentParser(description='AgenticSeek server script')
parser.add_argument('--model', type=str, help='Model to use. eg: deepseek-r1:14b', required=True)
args = parser.parse_args()

app = Flask(__name__)

model = args.model

# Shared state with thread-safe locks
class GenerationState:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_complete_sentence = ""
        self.current_buffer = ""
        self.is_generating = False

state = GenerationState()

def generate_response(history, model):
    global state
    print("using model:::::::", model)
    try:
        with state.lock:
            state.is_generating = True
            state.last_complete_sentence = ""
            state.current_buffer = ""

        stream = ollama.chat(
            model=model,
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
            ollama.pull(model)
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
        # Start generation in background thread
        threading.Thread(target=generate_response, args=(history, model)).start()
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
    app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)