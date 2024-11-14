import mongoose from "mongoose";

const outputSchema = new mongoose.Schema({
    email: {
        type:String,
        required: true
    },
    imagePath: {
        type: String,   // URL hoặc đường dẫn của ảnh không có mũ bảo hiểm
        required: true,
    },
    licensePlates: {
        type: String
    },  // Mảng lưu thông tin về các biển số
    timeStamp: {
        type: Date,
        default: Date.now,  // Thời gian lưu vào database
    },
});

const outputModel = mongoose.models.output || mongoose.model("output", outputSchema);

export default outputModel;
