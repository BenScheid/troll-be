from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/question", methods=["POST"])
def ask():
    if request.is_json:
        data = request.get_json()
        q = data.get('q')
        if not q:
            return jsonify({"error": "No question provided"}), 400

        try:
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You should just answer with 'Just don't have ' or 'Just don't be ' and whatever is said"},
                    {"role": "user", "content": q}
                ]
            )
            response = completion.choices[0].message.content
            return jsonify({"response": response})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
