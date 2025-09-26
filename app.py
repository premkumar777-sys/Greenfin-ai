from flask import Flask, request, jsonify, render_template
import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("api.env")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_AGENT_ID = os.getenv("AWS_AGENT_ID")

app = Flask(__name__)

# AWS Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/dash")
def dashboard():
    return render_template("dash.html")

@app.route("/eco")
def eco_tips():
    return render_template("eco.html")

# API endpoint for chatbot
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = bedrock_client.invoke_model(
            modelId=AWS_AGENT_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": user_message})
        )

        body = json.loads(response["body"].read().decode("utf-8"))
        agent_response = body.get("outputText") or body.get("completion") or str(body)
        return jsonify({"response": agent_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
