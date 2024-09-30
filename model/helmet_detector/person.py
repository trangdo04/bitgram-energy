import cv2
from ultralytics import YOLO
from PIL import Image, ImageDraw
import numpy as np
import os

model = YOLO('yolov8s.pt')
# Path to your video file
input_path = os.path.join(".\\data\\input")
output_path = os.path.join(".\\data\\output")
# Path to your video file
video_path = os.path.join(input_path,"input.mp4")
fixed_size = (640, 480) #fixed window size
cap = cv2.VideoCapture(video_path)

# Check successfully opened video
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the original frame dimensions and FPS of the video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Initialize VideoWriter object to save the output video
output_path = os.path.join(output_path,"output_video.mp4")  # Output file path
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

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

    # Process each detected object
    for result in results:
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            
            if class_id == 'person':
                # Get coordinates and confidence of the object
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = round(box.conf[0].item(), 2)
                
                # Draw bounding box
                draw.rectangle(cords, outline="red", width=2)
                
                # Add label and confidence
                label = f"{class_id} {conf}"
                draw.text((cords[0], cords[1] - 10), label, fill="red")

    # Convert PIL image back to OpenCV format (RGB -> BGR)
    annotated_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    resized_frame = cv2.resize(annotated_frame, fixed_size)
    # Write the processed frame to the output video
    out.write(annotated_frame)

    # Optionally, display the frame in a window
    cv2.imshow("Video", resized_frame)
    
    # Press 'q' to exit the video early
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
cap.release()
out.release()  # Save the output video file
cv2.destroyAllWindows()

print(f"Output video saved at {output_path}")
