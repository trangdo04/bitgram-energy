import outputModel from "./outputModel.js";

const saveOutput = async (req, res) => {
    const {noHelmet, licensePlate, timeStamp} = req.body;
        const newOutput = new outputModel({
            noHelmet: noHelmet,
            licensePlate: licensePlate,
            timeStamp: timeStamp
        })
    try {
        await newOutput.save()
        res.json({success: true, message: "Save successful"})
    } catch (error) {
        res.json({success: false, message: "Error"})
    }
}

export {saveOutput}