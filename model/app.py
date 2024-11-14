from flask import Flask, request, jsonify, send_from_directory
from tempfile import NamedTemporaryFile
from flask_cors import CORS
from helmet_detector.test import helmet_detect
from License_plate_detector.recognition.LP_recognition import get_LP_number
import numpy as np
import cv2
import torch
import uuid  # Đảm bảo nhập uuid
import os

app = Flask(__name__)
CORS(app)
# Đảm bảo thư mục 'output_frames' tồn tại
OUTPUT_FRAMES_DIR = 'output_frames'
os.makedirs(OUTPUT_FRAMES_DIR, exist_ok=True)

@app.route('/process-video', methods=['POST'])
def process_video():
    video_data = request.files['video']

    # Tạo file tạm thời để lưu video tải lên
    with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        # Lưu video tải lên vào file tạm thời
        video_data.save(temp_video_file.name)
        temp_video_path = temp_video_file.name  # Lưu đường dẫn video tạm thời để xử lý
        LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'D:\\Bit garam\\bitgram-energy\\model\\License_plate_detector\\checkpoint\\plate_detection.pt', force_reload=True)
        OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'D:\\Bit garam\\bitgram-energy\\model\\License_plate_detector\\checkpoint\\optical_character_recognition.pt', force_reload=True)

    try:
        # Xử lý video và lấy các frame không có mũ bảo hiểm
        no_helmet_frames = helmet_detect(temp_video_path)

        # Tạo danh sách để lưu các URL của hình ảnh
        results = []
        # Lưu các frame dưới dạng hình ảnh
        for i, frame in enumerate(no_helmet_frames):
            plates_information = get_LP_number(frame, LP_detect, OCR)
            for LP_info in plates_information:
                box, text = LP_info
                cv2.rectangle(frame, box[:2], box[2:], (36, 255, 12), 2)
                cv2.putText(frame, text, (box[0], box[1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

            plates_information = [{'box': box, 'text': text} for i, (box, text) in enumerate(plates_information)]

            unique_filename = str(uuid.uuid4()) + '.jpg'  # Sử dụng uuid ở đây

            processed_image_path = os.path.join(OUTPUT_FRAMES_DIR, unique_filename)
            cv2.imwrite(processed_image_path, frame)
            results.append({
                "image_path": processed_image_path,
                "plates": plates_information
            })  
        # Trả về danh sách URL hình ảnh trong response
        return jsonify({"message": "Video processed successfully", "results": results}), 200

    except Exception as e:
        print(f"Error processing video: {e}")
        return jsonify({"message": "Error processing video", "error": str(e)}), 500

    finally:
        # Dọn dẹp: Xóa video tạm thời
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

@app.route('/output_frames/<filename>')
def serve_file(filename):
    # Trả về tệp hình ảnh từ thư mục 'output_frames'
    return send_from_directory(OUTPUT_FRAMES_DIR, filename)
if __name__ == '__main__':
    app.run(port=5000)