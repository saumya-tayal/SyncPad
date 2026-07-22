from flask import Flask, jsonify, session
from flask import request
from flask_cors import CORS
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_super_secret_key"
CORS(app)

connection = None

try:
    connection = get_connection()
    print("Connected to MySQL!")

except Exception as e:
    print(e)

finally:
    if connection:
        connection.close()

@app.route("/hello")
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/documents")
def documents():
    if "user_id" not in session:
        return jsonify({"error": "Please login"}), 401
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM documents
            WHERE user_id = %s
            """,
            (session["user_id"],)
        )
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

@app.route("/documents", methods=["POST"])
def add_document():
    if "user_id" not in session:
        return jsonify({"error": "Please login"}), 401
    connection = None
    cursor = None
    try:
        data = request.get_json()
        title = data["title"]
        content = data["content"]
        connection = get_connection()
        cursor = connection.cursor()
        user_id = session["user_id"]
        cursor.execute(
            """
            INSERT INTO documents(title, content, user_id)
            VALUES(%s, %s, %s)
            """,
            (title, content, user_id)
        )
        connection.commit()
        return jsonify({
            "message": "Document created successfully"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route("/signup", methods=["POST"])
def signup():

    connection = None
    cursor = None

    try:
        data = request.get_json()

        email = data["email"]
        password = data["password"]

        hashed_password = generate_password_hash(password)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users(email, password)
            VALUES(%s, %s)
            """,
            (email, hashed_password)
        )

        connection.commit()

        return jsonify({"message": "User created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/login", methods=["POST"])
def login():
    connection = None
    cursor = None

    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        if check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return jsonify({"message": "Login successful"}), 200

        return jsonify({"error": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})

if __name__ == "__main__":
    app.run(debug=True)