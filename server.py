from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = "secret123"   

#generates tokens
@app.route("/generate", methods=["POST"])
def generate_token():
    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    expiration = datetime.utcnow() + timedelta(hours=1)

    payload = {
        "user_id": user_id,
        "exp": expiration
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

#verify
@app.route("/verify", methods=["POST"])
def verify_token():
    token = request.form.get("token")

    if not token:
        return jsonify({"error": "token is required"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "decoded": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


@app.route("/run_app", methods=["POST"])
def run_protected_application():
    token = request.form.get("token")

    if not token:
        return jsonify({"error": "token required"}), 400

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Application started successfully!"})
    except jwt.InvalidTokenError:
        return jsonify({"error": "Not authorized"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0")
