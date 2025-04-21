import cv2
import numpy as np
from retinaface.src.retinaface import RetinaFace
from deepface import DeepFace
import os
import sqlite3
import matplotlib.pyplot as plt


test_image_path = 'Image3.jpg'
img = cv2.imread(test_image_path)
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

model = RetinaFace()
faces = model.predict(rgb_img)


conn = sqlite3.connect('attendance.db')
c = conn.cursor()
c.execute('SELECT name, photo_path FROM students')
refs = {row[0]: row[1] for row in c.fetchall()}
conn.close()

results = []
threshold = 0.65
matched_students = set()

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
            photo_abs_path = os.path.join(ref_img_path)
            if not os.path.exists(photo_abs_path):
                continue

            result = DeepFace.verify(cropped_resized, photo_abs_path, model_name='Facenet', enforce_detection=False)
            print(f"Comparing with {name}: Distance {result['distance']:.3f}")

            if result['distance'] < lowest_distance:
                lowest_distance = result['distance']
                best_match = name
        except Exception as e:
            print(f"Error with {name}: {e}")

    if best_match and lowest_distance < threshold:
        print(f"✅ Face {i+1}: {best_match} (Distance: {lowest_distance:.3f})")
        results.append(best_match)
        matched_students.add(best_match)
        label = f"✅ {best_match}"
    else:
        print(f"❌ Face {i+1}: Unknown (Distance: {lowest_distance:.3f})")
        results.append("Unknown")
        label = f"❌ Unknown"

    # Draw on the image
    color = (0, 255, 0) if "✅" in label else (255, 0, 0)
    cv2.rectangle(rgb_img, (x1, y1), (x2, y2), color, 2)
    cv2.putText(rgb_img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=2.0, color=(255,255,255), thickness=7)
plt.figure(figsize=(16, 10))
plt.imshow(rgb_img)
plt.axis("off")
plt.title("Recognition Result")
plt.show()
