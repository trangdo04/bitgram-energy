import mongoose from "mongoose";

// key word export to allow access from server.js
export const connectDB = async() => {
    await mongoose.connect("mongodb+srv://22022638:NMJnbOuGrr2H5udZ@helmet.cluao.mongodb.net/detect-helmet").then(() => console.log("DB connected"));
}
