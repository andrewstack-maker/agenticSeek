#!/usr/bin python3

import logging
import argparse
from flask import Flask, jsonify, request

from sources.llamacpp import LlamacppLLM
from sources.ollama import OllamaLLM

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

parser = argparse.ArgumentParser(description='AgenticSeek server script')
parser.add_argument('--provider', type=str, help='LLM backend library to use. set to [ollama] or [llamacpp]', required=True)
parser.add_argument('--port', type=int, help='port to use', required=True)
args = parser.parse_args()

app = Flask(__name__)

generator = None

assert args.provider in ["ollama", "llamacpp"], f"Provider {args.provider} does not exists. see --help for more information"

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
    provider = args.provider
    if provider == "ollama":
        generator = OllamaLLM()
    elif provider == "llamacpp":
        generator = LlamacppLLM()
    else:
        raise ValueError(f"Provider {provider} does not exists. see --help for more information")
    if model is None:
        return jsonify({"error": "Model not provided"}), 400
    generator.set_model(model)
    return jsonify({"message": "Model set"}), 200

@app.route('/get_updated_sentence')
def get_updated_sentence():
    return generator.get_status()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=args.port)