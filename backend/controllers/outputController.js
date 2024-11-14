import outputModel from "../models/outputModel.js";

const saveOutput = async (req, res) => {
    const { email, imagePath, licensePlates, timeStamp } = req.body;

    const newOutput = new outputModel({
        email: email,
        imagePath: imagePath,
        licensePlates: licensePlates,  // Lưu mảng licensePlates
        timeStamp: timeStamp || Date.now(),
    });

    try {
        await newOutput.save();
        res.json({ success: true, message: "Save successful" });
    } catch (error) {
        console.error("Error saving output:", error.message);
        res.status(500).json({ success: false, message: "Error saving output" });
    }
};

const getHistory = async (req, res) => {
    const { email } = req.body;
    try {
        // Tìm tất cả các output có email khớp trong outputModel
        const history = await outputModel.find({ email });
        
        // Kiểm tra nếu không có kết quả
        if (!history || history.length === 0) {
            return res.status(404).json({ message: "No history found for this email" });
        }
        
        // Trả về tất cả output dưới dạng JSON
        res.status(200).json({ history });
    } catch (error) {
        console.error("Error retrieving history:", error);
        // Trả về lỗi nếu có vấn đề xảy ra trong quá trình truy vấn
        res.status(500).json({ message: "Server error. Could not retrieve history." });
    }
};

export { saveOutput, getHistory };
