from flask import Flask, request, jsonify, send_from_directory
from tempfile import NamedTemporaryFile
import os
import cv2
from flask_cors import CORS

from helmet_detector.helmet_detector import helmet_detect

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

    try:
        # Xử lý video và lấy các frame không có mũ bảo hiểm
        no_helmet_frames = helmet_detect(temp_video_path)
        
        # Tạo danh sách để lưu các URL của hình ảnh
        image_urls = []

        # Lưu các frame dưới dạng hình ảnh
        for i, frame in enumerate(no_helmet_frames):
            image_filename = os.path.join(OUTPUT_FRAMES_DIR, f"frame_{i + 1}.jpg")
            cv2.imwrite(image_filename, frame)  # Lưu frame dưới dạng hình ảnh
            image_urls.append(f"frame_{i + 1}.jpg")  # Thêm tên file vào danh sách

        # Trả về danh sách URL hình ảnh trong response
        return jsonify({"message": "Video processed successfully", "image_urls": image_urls}), 200
    
    except Exception as e:
        print(f"Error processing video: {e}")
        return jsonify({"message": "Error processing video", "error": str(e)}), 500
    
    finally:
        # Dọn dẹp: Xóa video tạm thời
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

<<<<<<< HEAD
    return result
=======
@app.route('/output_frames/<filename>')
def serve_file(filename):
    # Trả về tệp hình ảnh từ thư mục 'output_frames'
    return send_from_directory(OUTPUT_FRAMES_DIR, filename)
>>>>>>> 0f8a97ca66cfe76d396c59eb097e6ecefa16b2d4

if __name__ == '__main__':
    app.run(port=5000)
