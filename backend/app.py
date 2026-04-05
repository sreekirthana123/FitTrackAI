import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector


# Load ML models
try:
    weight_model = joblib.load('weight_model.pkl')
    sleep_model = joblib.load('sleep_model.pkl')
    scaler = joblib.load('scaler.pkl')
    models_loaded = True
except FileNotFoundError:
    weight_model = None
    sleep_model = None
    scaler = None
    models_loaded = False
    print("Warning: Model files not found. Predictions will not be available.")

app = Flask(__name__)
CORS(app)

# Database connection
def get_db():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root1234",
        database="fitness_db"
    )
    return connection

@app.route('/')
def home():
    return jsonify({"message": "FitTrack AI Backend is running! 💪"})

@app.route('/test-db')
def test_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        conn.close()
        return jsonify({"status": "Connected!", "tables": [t[0] for t in tables]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/register', methods=['POST'])
def register():
    try:
        from flask import request
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, age, gender, weight, height, email, contact, goal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['name'], data['age'], data['gender'],
            data['weight'], data['height'], data['email'],
            data['contact'], data['goal']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully! 🎉"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/log/workout', methods=['POST'])
def log_workout():
    try:
        from flask import request
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workouts (user_id, date, type, duration, calories, intensity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], data['date'], data['type'],
            data['duration'], data['calories'], data['intensity']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Workout logged successfully! 💪"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/log/meal', methods=['POST'])
def log_meal():
    try:
        from flask import request
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meals (user_id, date, food_name, calories, meal_type, water_ml)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], data['date'], data['food_name'],
            data['calories'], data['meal_type'], data['water_ml']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Meal logged successfully! 🍽️"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/log/health', methods=['POST'])
def log_health():
    try:
        from flask import request
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_logs (user_id, date, weight, sleep_hours, sleep_quality, steps, heart_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], data['date'], data['weight'],
            data['sleep_hours'], data['sleep_quality'],
            data['steps'], data['heart_rate']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Health logged successfully! ❤️"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/log/mental', methods=['POST'])
def log_mental():
    try:
        from flask import request
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mental_logs (user_id, date, mood, stress, energy_am, energy_pm, productivity, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['user_id'], data['date'], data['mood'],
            data['stress'], data['energy_am'], data['energy_pm'],
            data['productivity'], data['notes']
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Mental log saved successfully! 🧠"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/dashboard/<int:user_id>', methods=['GET'])
def dashboard(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM workouts WHERE user_id = %s ORDER BY date DESC LIMIT 7", (user_id,))
        workouts = cursor.fetchall()

        cursor.execute("SELECT * FROM meals WHERE user_id = %s ORDER BY date DESC LIMIT 7", (user_id,))
        meals = cursor.fetchall()

        cursor.execute("SELECT * FROM health_logs WHERE user_id = %s ORDER BY date DESC LIMIT 7", (user_id,))
        health = cursor.fetchall()

        cursor.execute("SELECT * FROM mental_logs WHERE user_id = %s ORDER BY date DESC LIMIT 7", (user_id,))
        mental = cursor.fetchall()

        conn.close()
        return jsonify({
            "user": user,
            "workouts": workouts,
            "meals": meals,
            "health": health,
            "mental": mental
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/predict/<int:user_id>', methods=['GET'])
def predict(user_id):
    try:
        if not models_loaded:
            return jsonify({"error": "ML models are not available. Please ensure weight_model.pkl, sleep_model.pkl, and scaler.pkl are in the backend directory."})
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT h.sleep_hours, h.steps, h.heart_rate, h.weight,
                   m.mood, m.stress, m.productivity,
                   me.calories calories_consumed, me.calories calories_burned
            FROM health_logs h
            JOIN mental_logs m ON h.user_id = m.user_id AND h.date = m.date
            JOIN meals me ON h.user_id = me.user_id AND h.date = me.date
            WHERE h.user_id = %s
            ORDER BY h.date DESC LIMIT 1
        """, (user_id,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return jsonify({"error": "No data found for this user. Please log your health data first!"})

        user_df = pd.DataFrame([data])

        predicted_weight = weight_model.predict(user_df[['sleep_hours', 'calories_consumed', 
                            'calories_burned', 'steps', 'heart_rate', 
                            'mood', 'stress', 'productivity']])[0]

        sleep_features = ['sleep_hours', 'stress', 'mood', 'productivity', 'heart_rate']
        sleep_scaled = scaler.transform(user_df[sleep_features])
        sleep_risk = sleep_model.predict(sleep_scaled)[0]

        if sleep_risk == 1:
            insight = f"⚠️ You only slept {data['sleep_hours']} hours and your stress is high. Your predicted weight tomorrow is {predicted_weight:.1f} kg. Try to sleep early tonight and take breaks during work!"
        else:
            insight = f"✅ You're doing great! Your predicted weight tomorrow is {predicted_weight:.1f} kg. Keep it up!"

        return jsonify({
            "predicted_weight": round(predicted_weight, 1),
            "sleep_risk": int(sleep_risk),
            "insight": insight
        })

    except Exception as e:
        return jsonify({"error": str(e)})
if __name__ == '__main__':
    app.run(debug=True)