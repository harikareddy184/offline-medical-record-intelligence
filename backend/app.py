from flask import Flask, request, jsonify
from flask_cors import CORS
from input_processor import process_input
from inference import run_inference
from output_formatter import format_output

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Medical AI Backend is Running"

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    text = data.get("text", "")

    processed = process_input({"input": text})
    result = run_inference(processed)
    output = format_output(processed, result)

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)