import torch
import torch.nn as nn
import os
from ultralytics import YOLO
import cv2

# Set up directory paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)

ckpt_path = os.path.join(current_dir, "ckpt", "helmet-detect-yolov8.pt")
input_path = 'D:\\VSC\\bitgram-energy\\model\\data\\input\\movie2.mp4'
# NOTE: modify this
output_dir = os.path.join(parent_dir, "data", "output", "no_helmet_motorcycles")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def helmet_detect(input_path):
    # Set up video capture
    cap = cv2.VideoCapture(input_path)

    # Load the YOLO model
    model = YOLO('D:\\VSC\\bitgram-energy\\model\\helmet_detector\\ckpt\\helmet-detect-yolov8.pt')

    # Initialize frame counter for naming output images
    frame_counter = 0

    # Get results from the model (streaming)
    results = model(source=input_path, stream=True)

    # Process video frames
    for r in results:
        frame = r.orig_img  # Get the original frame from the results
        if frame is None:
            break

        # Flags to check if motorcycle and helmet are detected
        motorcycle_detected = False
        no_helmet_detected = False

        # Process bounding boxes in the frame
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Get coordinates of bounding box
            class_id = box.cls[0].item()  # Get the class ID

            # Check if motorcycle (class_id == 0) and no helmet (class_id == 1 for no helmet)
            if class_id == 0:  # Assuming class ID 0 is for motorcycle
                motorcycle_detected = True
                color = (0, 255, 0)  # Green box for motorcycle
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # Draw bounding box

            elif class_id == 1:  # Assuming class ID 1 is for no helmet
                no_helmet_detected = True
                color = (0, 0, 255)  # Red box for no helmet
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # Draw bounding box

        # If a motorcycle is detected without a helmet, save the frame
        if motorcycle_detected and no_helmet_detected:
            frame_counter += 1
            output_image_path = os.path.join(output_dir, f"no_helmet_{frame_counter}.jpg")
            cv2.imwrite(output_image_path, frame)  # Save the image
            print(f"Saved frame with no helmet: {output_image_path}")

    # Release the video capture resource
    cap.release()

# Example usage
helmet_detect(input_path)
