from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/value', methods=['GET'])
def get_value():
    return jsonify({"value": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
