import numpy as np
import cv2
import torch
import uuid  # Đảm bảo nhập uuid
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from recognition import get_LP_number

app = Flask(__name__)
CORS(app)

PROCESSED_FRAMES_DIR = 'processed_frames'

if not os.path.exists(PROCESSED_FRAMES_DIR):
    os.makedirs(PROCESSED_FRAMES_DIR)

# LOAD MODEL
with app.app_context():
    LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoint/plate_detection.pt', force_reload=True)
    OCR = torch.hub.load('ultralytics/yolov5', 'custom', 'checkpoint/optical_character_recognition.pt', force_reload=True)


@app.post('/lp_recognition')
def recognize_lp():
    try:
        file = request.files['file']
    except KeyError:
        return {'message': 'Provide file for recognition!'}, 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    plates_information = get_LP_number(image, LP_detect, OCR)

    for LP_info in plates_information:
        box, text = LP_info
        cv2.rectangle(image, box[:2], box[2:], (36, 255, 12), 2)
        cv2.putText(image, text, (box[0], box[1]-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)

    plates_information = [{'box': box, 'text': text} for i, (box, text) in enumerate(plates_information)]

    # Tạo tên file duy nhất cho ảnh đã xử lý
    unique_filename = str(uuid.uuid4()) + '.jpg'  # Sử dụng uuid ở đây
    processed_image_path = os.path.join(PROCESSED_FRAMES_DIR, unique_filename)

    # Kiểm tra xem ảnh đã được ghi thành công chưa
    if not cv2.imwrite(processed_image_path, image):
        return jsonify({'message': 'Error saving the processed image!'}), 500

    return jsonify({
        'plates': plates_information,
        'image_path': unique_filename  # Trả về tên tệp duy nhất thay vì đường dẫn đầy đủ
    })


@app.route('/get_image/<image_path>', methods=['GET'])
def get_image(image_path):
    # Trả ảnh từ thư mục 'processed_frames' với tên file duy nhất
    return send_from_directory(PROCESSED_FRAMES_DIR, image_path)


if __name__ == '__main__':
    app.run(port=5001)
