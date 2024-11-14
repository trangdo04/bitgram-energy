import os
from ultralytics import YOLO
import cv2

# Define class IDs for motorbike and helmet
RIDER_CLASS_ID = 1  
HELMET_CLASS_ID = 2     
NO_HELMET_CLASS_ID = 3

# Create a directory to save images
output_dir = 'D:\\Bit garam\\bitgram-energy\\model\\data\\output'
os.makedirs(output_dir, exist_ok=True)
def helmet_detect(input_path):
    model = YOLO("D:\\Bit garam\\bitgram-energy\\model\\helmet_detector\\ckpt\\best.pt")
    results = model.predict(source=input_path, stream=True, save=True)
    list_image=[]
    # Process all results and save images
    frame_count = 0  # To keep track of frame numbers for unique image filenames
    for r in results:
        frame = r.orig_img

        # Get all motorbike boxes in the frame
        motorbike_boxes = [box for box in r.boxes if int(box.cls[0]) == RIDER_CLASS_ID]
        no_helmet_boxes = [box for box in r.boxes if int(box.cls[0]) == NO_HELMET_CLASS_ID]

        # Process each motorbike box and check if it has any overlapping "no helmet" box
        for motorbike_box in motorbike_boxes:
            x1, y1, x2, y2 = map(int, motorbike_box.xyxy[0])
            
            # Check for overlap with any "no helmet" box
            no_helmet_in_motorbike = any(
                (int(no_helmet_box.xyxy[0][0]) >= x1 and int(no_helmet_box.xyxy[0][2]) <= x2 and
                 int(no_helmet_box.xyxy[0][1]) >= y1 and int(no_helmet_box.xyxy[0][3]) <= y2)
                for no_helmet_box in no_helmet_boxes
            )

            # If a "no helmet" box is found within the motorbike box, save the motorbike crop
            if no_helmet_in_motorbike:
                cropped_img = frame[y1:y2, x1:x2]
                crop_filename = os.path.join(output_dir, f'no_helmet_{frame_count:04d}.jpg')
                cv2.imwrite(crop_filename, cropped_img)
                frame_count += 1
                list_image.append(cropped_img.copy())

    return list_image


# # # Test the function 
# input_path = 'D:\\Bit garam\\bitgram-energy\\model\\data\\input\\test.mp4'
# helmet_detect(input_path)