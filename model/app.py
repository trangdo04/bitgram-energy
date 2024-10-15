from flask import Flask, request
from helmet_detector.helmet_detector import helmet_detect

app = Flask(__name__)

@app.route('/process-video', methods=['POST'])
def process_video():
    video_data = request.files['video']
    result = helmet_detect(video_data)
    return 'Video processes successfully', 200

if __name__ == 'main':
    app.run(port=5001)