from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Restrict CORS to specific origin


@app.route('/api/value', methods=['POST'])
def post_value():
    data = request.json  # Get JSON data from the request
    value = data.get("value", "")  # Get the 'value' field from the JSON payload
    response = f"{value}2"  # Append '2' to the received value
    return jsonify({"response": response})  # Return the response

if __name__ == '__main__':
    app.run(debug=True)
