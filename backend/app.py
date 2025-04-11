from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# OpenAI API Key (replace with your actual key)
OPENAI_API_KEY = "your_openai_api_key"

# Handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Custom responses for specific commands
    if "your name" in user_input.lower() or "who are you" in user_input.lower():
        return jsonify({"response": "My name is ZOOR AI."})

    if user_input.lower() in ["hello", "hi", "hey"]:
        return jsonify({"response": "Hello! How can I assist you today?"})

    # Fetch response from OpenAI GPT API
    response = fetch_from_openai(user_input)
    return jsonify({"response": response})

def fetch_from_openai(prompt):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error fetching response from OpenAI: {e}")
        return "Sorry, I couldn't fetch the answer. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)