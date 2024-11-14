import mongoose from "mongoose";

const plateSchema = new mongoose.Schema({
    box: {
        type: [Number],  // Array để lưu tọa độ hộp, ví dụ: [x, y, width, height]
        required: true,
    },
    text: {
        type: String,   // Văn bản biển số được nhận diện
        required: true,
    },
});

const outputSchema = new mongoose.Schema({
    email: {
        type:String,
        required: true
    },
    imagePath: {
        type: String,   // URL hoặc đường dẫn của ảnh không có mũ bảo hiểm
        required: true,
    },
    licensePlates: [plateSchema],  // Mảng lưu thông tin về các biển số
    timeStamp: {
        type: Date,
        default: Date.now,  // Thời gian lưu vào database
    },
});

const outputModel = mongoose.models.output || mongoose.model("output", outputSchema);

export default outputModel;
