import gradio as gr
import requests

def detect(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get("http://127.0.0.1:5000/emotion", headers=headers)
    if res.status_code == 200:
        data = res.json()
        return f"Emotion: {data['emotion']} \nTip: {data['tip']}"
    return "Invalid token or error"

gr.Interface(
    fn=detect,
    inputs=gr.Textbox(label="JWT Token"),
    outputs="text",
    title="Emotion Detector",
).launch()
