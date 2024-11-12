from flask import Flask, request
from tempfile import NamedTemporaryFile
import os
from helmet_detector.helmet_detector import helmet_detect

app = Flask(__name__)

@app.route('/process-video', methods=['POST'])
def process_video():
    video_data = request.files['video']

    # Create a temporary file to save the uploaded video
    with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        # Save the uploaded video to the temporary file
        video_data.save(temp_video_file.name)
        temp_video_path = temp_video_file.name  # Store the path for processing

    try:
        # Call the helmet detection function with the temporary video path
        result = helmet_detect(temp_video_path)
        
        # Process the result as needed (e.g., return a response)
        return 'Video processed successfully', 200
    
    except Exception as e:
        print(f"Error processing video: {e}")
        return 'Error processing video', 500
    
    finally:
        # Clean up: Remove the temporary video file
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

    return result

if __name__ == '__main__':
    app.run(port=5000)