from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/value', methods=['GET'])
def get_value():
    return jsonify({"value": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
