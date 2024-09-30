import cv2
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Load YOLOv8 model
model = YOLO('yolov8s.pt')

input_path = os.path.join(".\\data\\input")
output_path = os.path.join(".\\data\\output")

# Path to your video file
video_path = os.path.join(input_path,"input.mp4")
cap = cv2.VideoCapture(video_path)

# from IPython import embed
# embed()

# Check if the video was successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Desired fixed window size (width, height)
fixed_size = (640, 480)

# Loop through the frames of the video
while True:
    ret, frame = cap.read()  # Read a frame from the video
    if not ret:
        print("Reached the end of the video.")
        break

    # Perform object detection using YOLOv8
    results = model(frame)

    # Convert the OpenCV BGR frame to a PIL image for drawing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    pil_image = Image.fromarray(frame_rgb)
    draw = ImageDraw.Draw(pil_image)
    target_classes = ['motorcycle', 'person']
    # Process each detected object
    for result in results:
        # Loop through detected objects and filter only 'motorcycle' and 'person'
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]

            if class_id in target_classes:
                # Get coordinates and confidence of the detected object
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = round(box.conf[0].item(), 2)

                # Draw bounding box (red for motorcycle, blue for person)
                outline_color = "red" if class_id == "motorcycle" else "blue"
                draw.rectangle(cords, outline=outline_color, width=2)

                # Add label and confidence
                label = f"{class_id} {conf}"
                draw.text((cords[0], cords[1] - 10), label, fill=outline_color)

    # Convert PIL image back to OpenCV format (RGB -> BGR)
    annotated_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Resize the frame to the fixed size
    resized_frame = cv2.resize(annotated_frame, fixed_size)
    
    # Display the resized frame in a window
    cv2.imshow("Video", resized_frame)
    
    # Wait for 25 ms before displaying the next frame
    # Press 'q' to exit the video early
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()
