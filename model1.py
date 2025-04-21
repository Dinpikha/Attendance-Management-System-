import cv2
import mediapipe as mp


img = cv2.imread('Image5.jpg')
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

results = face_detection.process(rgb_img)


if results.detections:
    for det in results.detections:
        bbox = det.location_data.relative_bounding_box
        h, w, _ = img.shape
        x, y = int(bbox.xmin * w), int(bbox.ymin * h)
        w_box, h_box = int(bbox.width * w), int(bbox.height * h)
        cv2.rectangle(img, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
else:
    print("No faces detected 😭")


scale_percent = 40
new_width = int(img.shape[1] * scale_percent / 100)
new_height = int(img.shape[0] * scale_percent / 100)
resized = cv2.resize(img, (new_width, new_height))

cv2.imshow("Faces", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
