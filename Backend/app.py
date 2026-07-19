from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/hello")
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/documents")
def documents():
    return jsonify([
        {
            "id": 1,
            "title": "Computer Networks"
        },
        {
            "id": 2,
            "title": "DBMS Notes"
        },
        {
            "id": 3,
            "title": "Placement Prep"
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)