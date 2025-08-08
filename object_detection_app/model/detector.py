from ultralytics import YOLO
import cv2
import numpy as np
import json
import os

model = YOLO("yolov8n-seg.pt")

# Load category colors
legend_path = os.path.join("assets", "legend_colors.json")
with open(legend_path, "r") as f:
    CATEGORY_COLORS = json.load(f)

    
def process_frame(image, user_colors=None):
    if image is None:
        return np.zeros((300, 300, 3), dtype=np.uint8), {}

    results = model.predict(image, task="segment", verbose=False)[0]
    final = image.copy()
    names = model.names

    boxes = results.boxes
    masks = results.masks.data.cpu().numpy() if results.masks is not None else []

    counts = {}

    for i, box in enumerate(boxes):
        cls_id = int(box.cls[0])
        label = names[cls_id]
        counts[label] = counts.get(label, 0) + 1

        color = user_colors.get(label) if user_colors else None
        if color is None:
            color = CATEGORY_COLORS.get(label, CATEGORY_COLORS["default"])

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        cv2.rectangle(final, (x1, y1), (x2, y2), color, 2)
        cv2.putText(final, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if i < len(masks):
            mask = masks[i]
            mask_resized = cv2.resize(mask.astype("float32"), (image.shape[1], image.shape[0]))
            colored_mask = np.zeros_like(image)
            for c in range(3):
                colored_mask[:, :, c] = (mask_resized * color[c]).astype(np.uint8)
            final = cv2.addWeighted(final, 1, colored_mask, 0.5, 0)

    return final, counts
