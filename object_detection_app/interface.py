import gradio as gr
import json
from model.detector import process_frame
import cv2

# Load default categories
with open("assets/legend_colors.json") as f:
    DEFAULT_COLORS = json.load(f)
    DEFAULT_COLORS.pop("default", None)  # Remove fallback for UI

def hex_to_rgb(hex_color):
    try:
        hex_color = hex_color.strip().lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("Invalid hex color length")
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    except Exception as e:
        print(f"[ERROR] Invalid color '{hex_color}', using default red. ({e})")
        return [255, 0, 0]  # Fallback to red

def wrap_html_legend(color_map):
    legend_html = "<ul style='font-size:16px;'>"
    for label, color in color_map.items():
        hex_color = '#%02x%02x%02x' % tuple(color)
        legend_html += f"<li><span style='color:{hex_color}'>⬤</span> {label}</li>"
    legend_html += "</ul>"
    return legend_html

def run_detection_image(image, person_color, car_color, dog_color):
    print(f"[DEBUG] Colors: person={person_color}, car={car_color}, dog={dog_color}")

    user_colors = {
        "person": hex_to_rgb(person_color),
        "car": hex_to_rgb(car_color),
        "dog": hex_to_rgb(dog_color)
    }

    result_img, counts = process_frame(image, user_colors)

    # Convert counts dict to readable text
    count_text = "\n".join([f"{k}: {v}" for k, v in counts.items()])

    return result_img, count_text


def run_detection_webcam(person_color, car_color, dog_color):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None

    user_colors = {
        "person": hex_to_rgb(person_color),
        "car": hex_to_rgb(car_color),
        "dog": hex_to_rgb(dog_color)
    }
    return process_frame(frame, user_colors)

with gr.Blocks() as demo:
    gr.Markdown("## 🎯 Custom Object Detection")
    gr.Markdown("Choose custom colors for each category")

    with gr.Row():
        person_color = gr.ColorPicker(label="Person", value="#FF0000")
        car_color = gr.ColorPicker(label="Car", value="#00FF00")
        dog_color = gr.ColorPicker(label="Dog", value="#FFFF00")

    with gr.Tab("📷 Image"):
        img_input = gr.Image(type="numpy", label="Upload an image")
        img_output = gr.Image(type="numpy", label="Detected output")
        count_output = gr.Textbox(label="Object Counts")

        detect_btn = gr.Button("Run Detection")
        detect_btn.click(
            fn=run_detection_image,
            inputs=[img_input, person_color, car_color, dog_color],
            outputs=[img_output, count_output]  # ✅ fix here
    )

    with gr.Tab("🎥 Webcam"):
        cam_output = gr.Image(type="numpy", label="Webcam Detection")
        cam_btn = gr.Button("📸 Capture & Detect")
        cam_btn.click(fn=run_detection_webcam, inputs=[person_color, car_color, dog_color], outputs=cam_output)

    with gr.Accordion("🎨 Legend", open=True):
        gr.HTML(wrap_html_legend(DEFAULT_COLORS))

demo.launch()
