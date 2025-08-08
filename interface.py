import gradio as gr
import cv2
import time
from deepface import DeepFace

tips = {
    "happy": "Keep smiling! Try spreading positivity.",
    "sad": "Take a walk or talk to a friend.",
    "angry": "Breathe deeply. Maybe meditate?",
    "surprise": "Reflect and journal your feelings.",
    "fear": "Talk to someone or listen to calming music.",
    "disgust": "Focus on something uplifting.",
    "neutral": "Keep going! Stay balanced.",
    "error": "Couldn't detect emotion. Try again."
}





def webcam_emotion_stream():
    cap = cv2.VideoCapture(0)
    last_time = 0
    emotion = "Waiting..."
    tip = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_time > 5:
            try:
                result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
                emotion = result[0]["dominant_emotion"].lower()
                tip = tips.get(emotion, "Stay positive!")
            except Exception as e:
                print("[ERROR]", e)
                emotion = "Error"
                tip = tips["error"]
            last_time = current_time

        cv2.putText(frame, f"Emotion: {emotion}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        yield frame, f"{emotion.capitalize()}", tip

    cap.release()
    cv2.destroyAllWindows()

def analyze_image_once(image):
    try:
        result = DeepFace.analyze(image, actions=["emotion"], enforce_detection=False)
        emotion = result[0]["dominant_emotion"].lower()
        return f"Detected Emotion: {emotion.capitalize()}", tips.get(emotion, "Stay positive!")
    except Exception as e:
        print("[ERROR]", e)
        return "Detected Emotion: Error", tips["error"]







with gr.Blocks(title="Emotion Health Analyzer") as demo:
    gr.Markdown("Emotion Health Analyzer")
    gr.Markdown("Live monitoring every 5 seconds or upload a photo for one-time check.")

    with gr.Tab("Real-Time Webcam Monitoring"):
        cam_output = gr.Image(label="Live Webcam Feed", show_label=False)
        emotion_text = gr.Textbox(label="Detected Emotion")
        tip_text = gr.Textbox(label="Mental Health Tip")
        start_btn = gr.Button("Start Monitoring")

        start_btn.click(fn=webcam_emotion_stream, outputs=[cam_output, emotion_text, tip_text])

    with gr.Tab("Analyze One Image"):
        image_input = gr.Image(label="Upload or Capture Image", type="numpy")
        single_emotion = gr.Textbox(label="Detected Emotion")
        single_tip = gr.Textbox(label="Mental Health Tip")
        analyze_btn = gr.Button("Analyze Emotion")

        analyze_btn.click(fn=analyze_image_once, inputs=image_input, outputs=[single_emotion, single_tip])

if __name__ == "__main__":
    demo.launch()
