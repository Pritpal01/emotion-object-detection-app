from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from model.detect_emotion import detect_emotion_from_frame
from database import emotions_col
from auth import auth_bp
from datetime import datetime
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# Register Blueprint for auth
app.register_blueprint(auth_bp, url_prefix="/auth")

# Emotion Route
@app.route("/emotion", methods=["GET"])
@jwt_required()
def get_emotion():
    username = get_jwt_identity()
    emotion = detect_emotion_from_frame()

    data = {
        "username": username,
        "emotion": emotion,
        "timestamp": datetime.utcnow()
    }
    emotions_col.insert_one(data)

    tips = {
        "happy": "Keep smiling! Try spreading positivity.",
        "sad": "Take a walk or talk to a friend.",
        "angry": "Breathe deeply. Maybe meditate?",
        "neutral": "Keep going! Stay balanced."
    }

    return jsonify({"emotion": emotion, "tip": tips.get(emotion.lower(), "Stay positive!")})


# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
