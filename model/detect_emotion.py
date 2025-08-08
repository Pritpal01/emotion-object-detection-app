import cv2
from deepface import DeepFace

def detect_emotion_from_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible")
        return "Camera Error"

    try:
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Frame read failed")
            return "Frame Error"

        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        emotion = result[0]["dominant_emotion"]
        region = result[0]["region"]

        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow("Emotion Detection", frame)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        return emotion.capitalize()

    except Exception as e:
        print("[ERROR] Detection failed:", e)
        return "Detection Error"