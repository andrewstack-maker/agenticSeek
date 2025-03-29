#!/usr/bin python3

import logging
import argparse
from flask import Flask, jsonify, request

from sources.llamacpp import LlamacppLLM
from sources.ollama import OllamaLLM

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

parser = argparse.ArgumentParser(description='AgenticSeek server script')
args = parser.parse_args()

app = Flask(__name__)

generator = None

@app.route('/generate', methods=['POST'])
def start_generation():
    if generator is None:
        return jsonify({"error": "Generator not initialized"}), 400
    data = request.get_json()
    history = data.get('messages', [])
    if generator.start(history):
        return jsonify({"message": "Generation started"}), 202
    return jsonify({"error": "Generation already in progress"}), 400

@app.route('/setup', methods=['POST'])
def setup():
    data = request.get_json()
    model = data.get('model', None)
    provider = data.get('provider', None)
    if provider is not None and generator is None:
        if provider == "ollama":
            generator = OllamaLLM()
        elif provider == "llamacpp":
            generator = LlamacppLLM()
        else:
            return jsonify({"error": "Provider not supported
    if model is None:
        return jsonify({"error": "Model not provided"}), 400
    generator.set_model(model)
    return jsonify({"message": "Model set"}), 200

@app.route('/get_updated_sentence')
def get_updated_sentence():
    return generator.get_status()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=3333)