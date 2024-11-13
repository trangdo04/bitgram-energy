import os
from ultralytics import YOLO
import cv2

# Define class IDs for motorbike and helmet
MOTORBIKE_CLASS_ID = 1  
HELMET_CLASS_ID = 2     
NO_HELMET_CLASS_ID = 3

# Create a directory to save images
output_dir = 'D:\\1\\Hacka\\bitgram-energy\\model\\data\\output'
os.makedirs(output_dir, exist_ok=True)
def helmet_detect(input_path):
    model = YOLO("D:\\1\\Hacka\\bitgram-energy\\model\\helmet_detector\\ckpt\\best.pt")
    results = model.predict(source=input_path, stream=True, save=True)
    list_image=[]
    # Process all results and save images
    frame_count = 0  # To keep track of frame numbers for unique image filenames
    for r in results:
        frame = r.orig_img
        contains_motorbike_without_helmet = False

        # Check each detected box
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get the class ID of the detected object

            if class_id == MOTORBIKE_CLASS_ID:
                # Check if there is no helmet in the same frame
                if not any(int(b.cls[0]) == HELMET_CLASS_ID for b in r.boxes):
                    contains_motorbike_without_helmet = True
                    break  # Stop checking once confirmed

        # Save only frames with motorbikes without helmets as images
        if contains_motorbike_without_helmet:
            frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
            list_image.append(frame.copy())
    print(f"Images with motorbikes without helmets saved in {output_dir}")
    return list_image

# Test the function 
input_path = 'D:\\1\\Hacka\\bitgram-energy\\model\\data\\input\\movie2.mp4'
helmet_detect(input_path)