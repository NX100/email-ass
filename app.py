from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load your API key from environment variable
openai.api_key = os.getenv("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")

# Pretty homepage served by Flask
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Route to serve the app UI
@app.route("/app", methods=["GET"])
def launch_app():
    return render_template("index.html")

# API endpoint to generate email replies
@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    email = data.get("email")

    prompt = f"""
    You are an expert email assistant. Read the email below and generate a polite and professional response:

    "{email}"

    Keep the reply concise and contextually appropriate.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        reply = response.choices[0].message["content"]
        return jsonify({"result": reply})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
