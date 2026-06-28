from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running"

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    result = {
        "status": "success",
        "message": "Request received",
        "input": data
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)