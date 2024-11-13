import outputModel from "./outputModel.js";

const saveOutput = async (req, res) => {
    const { noHelmet, licensePlates, timeStamp } = req.body;

    const newOutput = new outputModel({
        noHelmet: noHelmet,
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

export { saveOutput };
