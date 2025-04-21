import face_recognition
import cv2
import numpy as np


def preprocessimage(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at path '{image_path}' could not be loaded.")

    
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)

  
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    return image



sharpened_bgr = preprocessimage("dip.jpeg")
sharpened_rgb = cv2.cvtColor(sharpened_bgr, cv2.COLOR_BGR2RGB)

known_image = face_recognition.load_image_file("deep.jpeg")
known_encodings = face_recognition.face_encodings(known_image)

if not known_encodings:
    raise ValueError("No face found in known image.")

known_encoding = known_encodings[0]

# Detect faces in classroom image
face_locations = face_recognition.face_locations(sharpened_rgb)
face_encodings = face_recognition.face_encodings(sharpened_rgb, face_locations)

print(f"\nDetected {len(face_encodings)} face(s) in classroom image.")
for idx, face_encoding in enumerate(face_encodings):
    distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
    match_percentage = (1 - distance) * 100
    # print(f"Face {idx + 1} match: {match_percentage:.2f}%")

    
    
    
    match_percentage = (1 - distance) * 100
    if match_percentage > 50:  # Adjust this threshold (e.g., 50% or 60%)
        print(f"Face{idx+1} match: {match_percentage:.2f}% → ✅ ATTENDANCE MARKED")
    else:
        print(f"Face{idx+1} match: {match_percentage:.2f}% → ❌ NO MATCH")
    


