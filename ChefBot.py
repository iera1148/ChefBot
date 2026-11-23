from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import random
from openai import OpenAI
from dotenv import load_dotenv

# 1. SETUP DIRECTORIES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

# 2. LOAD ENVIRONMENT VARIABLES
load_dotenv(os.path.join(BASE_DIR, "app.env"))

# 3. INITIALIZE OPENAI CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"

# 4. APP & DATABASE CONFIGURATION
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(INSTANCE_DIR, 'chefbot.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 5. DATABASE MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)


with app.app_context():
    db.create_all()

# 6. SYSTEM PERSONA (FIXED MULTI-LINE SYNTAX)
persona = """
You are 'ChefBot', a friendly and creative Malaysian culinary assistant for Malaysian teens (11-19). 
Your goal is to help users cook delicious meals and reduce food waste. 

YOU SPECIALIZE IN:
- 'Peti Sejuk Surprise': Suggesting recipes based on leftover ingredients.
- Kitchen Science: Explaining why bread rises or how to fix salty soup.
- Malaysian Flavors: Expert knowledge in Nasi Goreng, Sambal, and local street food.

Use a fun, encouraging tone. Use simple cooking terms. 
Mix in some Malay words like 'Alamak', 'Sedap', and 'Jom', "Mantap Bossku". 
If a user is missing an ingredient, suggest a substitute. 
Always end with a small tip like 'Don't forget to wash your hands!'
"""


# 7. ROUTES
@app.route("/")
def home():
    return render_template("index_ChefBot.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": user_input}
            ],
            max_tokens=250
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        bot_response = "Alamak! Dapur saya berasap (Internal Error). Cuba lagi nanti!"

    # Update or create guest user
    user = User.query.filter_by(username="guest").first()
    if not user:
        user = User(username="guest")
        db.session.add(user)

    user.points += 5
    db.session.commit()

    return jsonify({"response": bot_response, "points": user.points})


@app.route("/award_points", methods=["POST"])
def award_points():
    data = request.json
    points_to_add = data.get("points", 0)

    user = User.query.filter_by(username="guest").first()
    if not user:
        user = User(username="guest")
        db.session.add(user)

    user.points += points_to_add
    db.session.commit()

    return jsonify({"new_points": user.points})


# 8. RUN APP
if __name__ == "__main__":
    app.run(debug=True)