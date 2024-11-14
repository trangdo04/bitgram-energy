import os
from ultralytics import YOLO
import cv2

# Define class IDs for motorbike and helmet
RIDER_CLASS_ID = 1  
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
        # Get all motorbike boxes in the frame
        motorbike_boxes = [box for box in r.boxes if int(box.cls[0]) == RIDER_CLASS_ID]

        # Check if any "no helmet" class exists in the frame
        no_helmet_exists = any(int(box.cls[0]) == NO_HELMET_CLASS_ID for box in r.boxes)

        # If there are motorbike boxes and a "no helmet" detection, save the motorbike crops
        if motorbike_boxes and no_helmet_exists:
            for motorbike_box in motorbike_boxes:
                x1, y1, x2, y2 = map(int, motorbike_box.xyxy[0])
                # xx1,yy1,xx2,yy2 = map(int, no_helmet_exists.xyxy[0])
                # color = (0, 0, 255)  # Red color for the bounding box
                # cv2.rectangle(frame, (xx1, yy1), (xx2, yy2), color, 2)
                cropped_img = frame[y1:y2, x1:x2]
                # Save the cropped image with a unique filename
                crop_filename = os.path.join(output_dir, f'no_helmet_{frame_count:04d}.jpg')
                list_image.append(cropped_img.copy())
                cv2.imwrite(crop_filename, cropped_img)
                frame_count += 1
    return list_image


# # Test the function 
# input_path = 'D:\\1\\Hacka\\bitgram-energy\\model\\data\\input\\input2.mp4'
# helmet_detect(input_path)