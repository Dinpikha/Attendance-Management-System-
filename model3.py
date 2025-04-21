import cv2
import numpy as np
from retinaface.src.retinaface import RetinaFace
from deepface import DeepFace
import base64
import os
from flask_cors import CORS 
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from SMTP import send_attendance_alert  # Your custom email function
import matplotlib.pyplot as plt  # <-- for displaying result

app = Flask(__name__)
CORS(app) 
app.secret_key = 'y'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'student_photos')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE,
                  password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  photo_path TEXT)''')
    conn.commit()
    conn.close()
init_db()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    session['logged_in'] = True
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Email already exists.")
        return redirect(url_for('home'))
    finally:
        conn.close()
    session['logged_in'] = True
    return redirect(url_for('dashboard'))

@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files['photo']
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Use RetinaFace once
    model = RetinaFace()
    faces = model.predict(rgb_img)

    # Load reference data
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT name, photo_path FROM students')
    refs = {row[0]: row[1] for row in c.fetchall()}
    conn.close()

    threshold = 0.65
    matched_students = set()
    present_students = []
    face_results = []
    recognized_count = 0
    unknown_count = 0

    for i, face in enumerate(faces):
        print(f"\n--- Face {i+1} ---")
        x1, y1, x2, y2 = face['x1'], face['y1'], face['x2'], face['y2']
        cropped = rgb_img[max(0, y1):y2, max(0, x1):x2]
        cropped_resized = cv2.resize(cropped, (160, 160))

        best_match = None
        lowest_distance = float('inf')

        for name, ref_img_path in refs.items():
            if name in matched_students:
                continue

            try:
                photo_abs_path = os.path.join(app.root_path, ref_img_path)
                if not os.path.exists(photo_abs_path):
                    print(f"Missing file: {photo_abs_path}")
                    continue

                result = DeepFace.verify(cropped_resized, photo_abs_path, model_name='Facenet', enforce_detection=False)
                print(f"Comparing with {name}: Distance {result['distance']:.3f}")

                if result['distance'] < lowest_distance:
                    lowest_distance = result['distance']
                    best_match = name
            except Exception as e:
                print(f"Error with {name}: {e}")

        if best_match and lowest_distance < threshold:
            matched_students.add(best_match)
            present_students.append(best_match)
            recognized_count += 1
            confidence = max(0, min(100, round((1 - (lowest_distance / threshold)) * 100, 1)))
            face_results.append({
                "label": best_match,
                "status": "recognized"
            })
            print(f"✅ Face {i+1}: {best_match} (Distance: {lowest_distance:.3f})")
        else:
            unknown_count += 1
            confidence = max(0, min(100, round((1 - (lowest_distance / threshold)) * 100, 1)))
            face_results.append({
                "label": best_match,
                "status": "recognized"
            })

            print(f"❌ Face {i+1}: Unknown (Lowest distance: {lowest_distance:.3f})")

    # Save attendance
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    for student_name in present_students:
        c.execute("SELECT id FROM students WHERE name=?", (student_name,))
        student_id_row = c.fetchone()
        if student_id_row:
            student_id = student_id_row[0]
            c.execute("INSERT OR IGNORE INTO attendance (student_id, status) VALUES (?, 'present')", (student_id,))

    c.execute("INSERT INTO attendance_logs (recognized, unknown) VALUES (?, ?)", (recognized_count, unknown_count))
    conn.commit()
    conn.close()

    # Optional: Alert for unknown faces
    if unknown_count > 0:
        send_attendance_alert("Unknown face(s) detected!")

    return jsonify({
        "faces": face_results,
        "recognized_count": recognized_count,
        
        "total_students": len(refs)
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)




