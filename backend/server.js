import express from 'express'
import multer from 'multer'
import path from 'path'
import cors from 'cors'
import { connectDB } from './config/database.js'
import outputRouter from './outputRoute.js'
import FormData from 'form-data';

// initialize app
const app = express()
// define which port the server will be lauched on
const port = 4000

// set up multer for handling file uploads
const storage = multer.memoryStorage();
const upload = multer({storage});

app.post('/upload-video', upload.single('video'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: 'No video file uploaded.' });
    }

    const videoBuffer = req.file.buffer;
    const formData = new FormData();
    formData.append('video', videoBuffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype,
    });

    try {
        const response = await axios.post('http://localhost:5000/process-video', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        return res.status(200).json({
            message: 'Video uploaded and processed successfully',
            data: response.data,
        });
    } catch (error) {
        console.error('Error sending video to Python model:', error.message);
        return res.status(500).json({ message: 'Error processing video.' });
    }
});


app.use(express.json())
app.use(cors())
// api to handle output from model
app.use("/api/output", outputRouter)

// uncomment below line to connect to DB
// connectDB();

// check with api
app.get("/",(req, res)=>{
    res.send("API working")
})


app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
})

