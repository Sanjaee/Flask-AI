import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


port = int(os.getenv("PORT", 3000))

@app.route('/v1/chat', methods=['POST'])
def chat_completion():
    try:
        data = request.get_json()
        message_content = data.get("content")

        if not message_content:
            return jsonify({"error": "Content field is required"}), 400

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
            model="llama3-8b-8192",
        )

        response = chat_completion.choices[0].message.content
        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    app.run(debug=True, port=port)
