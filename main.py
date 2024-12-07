from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/api/value', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:5173")
def post_value():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    # Handle POST request
    data = request.json
    value = data.get("value", "")
    response = f"{value}2"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
