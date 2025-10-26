from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='.')

# Ollama local API
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:latest"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        payload = {
            "model": MODEL,
            "prompt": user_message,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        text = result.get("response") or result.get("text") or "(no reply)"

        return jsonify({"reply": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
