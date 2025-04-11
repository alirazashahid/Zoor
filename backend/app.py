from flask import Flask, request, jsonify
from flask_cors import CORS
from data_upload import process_video, process_screenshot, process_text_file
from ai_model import train_model, generate_response
from formal_chat_data import get_formal_chat_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Pre-train the chatbot with formal chat data
@app.route('/pretrain-formal-chat', methods=['POST'])
def pretrain_formal_chat():
    data = get_formal_chat_data()
    train_model(data)
    return jsonify({"message": "Formal chat training complete!"})

# Handle additional data uploads for training
@app.route('/upload-data', methods=['POST'])
def upload_data():
    data_type = request.form.get("type")
    if not data_type:
        return jsonify({"error": "Data type missing"}), 400

    if data_type == "video":
        video_url = request.form.get("content")
        if not video_url:
            return jsonify({"error": "Video URL missing"}), 400
        transcript = process_video(video_url)
    elif data_type == "screenshot":
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Screenshot file missing"}), 400
        transcript = process_screenshot(file)
    elif data_type == "text":
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Text file missing"}), 400
        transcript = process_text_file(file)
    else:
        return jsonify({"error": "Invalid data type"}), 400

    if transcript:
        train_model(transcript)
        return jsonify({"message": "Training complete!"})
    return jsonify({"error": "Failed to process data"}), 500

# Handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = generate_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)