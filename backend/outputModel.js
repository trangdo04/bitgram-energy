import mongoose from "mongoose";

const outputSchema = new mongoose.Schema({
    noHelmet: {type: String, require: true},
    licensePlate: {type: String},
    timeStamp: {type: Date, default: Date.now}
})

const outputModel = mongoose.models.output || mongoose.model("output", outputSchema)

export default outputModel;