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

# NOTE: modify this
# input_path = 'D:\\VSC\\bitgram-energy\\model\\data\\input\\movie2.mp4'
output_dir = "D:\\VSC\\bitgram-energy\\model\\data\\output"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def helmet_detect(input_path):
    # Set up video capture
    cap = cv2.VideoCapture(input_path)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Desired frame processing rate (3-4 FPS)
    desired_fps = 4
    frames_to_skip = int(fps / desired_fps)  # Calculate how many frames to skip
    
    # Load the YOLO model
    model = YOLO('D:\\VSC\\bitgram-energy\\model\\helmet_detector\\ckpt\\helmet-detect-yolov8.pt')

    # Initialize frame counter for naming output images
    frame_counter = 0
    processed_counter = 0  # Counter to keep track of the processed frames

    # Create a list to hold frames with no-helmet motorcycles
    no_helmet_frames = []

    # Get results from the model (streaming)
    results = model(source=input_path, stream=True)

    # Process video frames
    for r in results:
        frame = r.orig_img  # Get the original frame from the results
        if frame is None:
            break

        # Skip frames to maintain processing speed at 3-4 frames per second
        if processed_counter % frames_to_skip != 0:
            processed_counter += 1
            continue  # Skip this frame
        
        processed_counter += 1

        # Create a dictionary to track motorcycles and their helmet status
        motorcycles = {}

        # Process bounding boxes in the frame
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Get coordinates of bounding box
            class_id = box.cls[0].item()  # Get the class ID

            # Assuming class ID 0 is for motorcycle and class ID 1 is for no helmet
            if class_id == 0:  # Motorcycle detected
                motorcycles[(x1, y1, x2, y2)] = False  # Initialize as wearing a helmet
            elif class_id == 1:  # No helmet detected
                motorcycles[(x1, y1, x2, y2)] = True  # Mark as no helmet

        # Only store frames that contain motorcycles without helmets
        for (x1, y1, x2, y2), no_helmet in motorcycles.items():
            if no_helmet:
                frame_counter += 1
                color = (0, 0, 255)  # Red box for no helmet
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # Draw bounding box

                # Append the frame with the motorcycle without helmet to the list
                no_helmet_frames.append(frame.copy())
                print(f"Added frame with no helmet to list: Frame {frame_counter}")

    # Release the video capture resource
    cap.release()

    # Return the list of frames with no-helmet motorcycles
    return no_helmet_frames

# Example usage
# no_helmet_images = helmet_detect(input_path)

# Print the number of frames found with no-helmet motorcycles
# print(f"Total frames with no-helmet motorcycles: {len(no_helmet_images)}")

