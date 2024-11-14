import React, { useState } from 'react';
import axios from 'axios';
import './input.css';
const Input = () => {
    const [video, setVideo] = useState(null);
    const [input, setInput] = useState(null);
    const [image, setImage] = useState([]); // Renamed to imageUrls for clarity
    const [output, setOutput] = useState([]); // Initialize output state

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.includes('video')) {
            const videoURL = URL.createObjectURL(file);
            setVideo(videoURL);
            setInput(file);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.includes('video')) {
            const videoURL = URL.createObjectURL(file);
            setVideo(videoURL);
            setInput(file);
        }
    };

    const clickButton = async () => {
        const formData = new FormData();
        formData.append('video', input);

        try {
            const response = await axios.post('http://localhost:5000/process-video', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            const plates = []

            if (response.status === 200) {
                const results = response.data.results;
                for (const result of results){
                    const newPlate = result.plates
                    const imagePath = result.image_path
                    if (newPlate.length > 0 && newPlate[0].text.length > 6) {
                        const newPlateText = newPlate[0].text;

                        // Kiểm tra nếu biển số là chuỗi con của bất kỳ biển số nào trong plates
                        const isPlateDuplicate = plates.some((existingPlateText) => 
                            existingPlateText.includes(newPlateText) || newPlateText.includes(existingPlateText)
                        );

                        if (!isPlateDuplicate) {
                            plates.push(newPlateText); 
                            await axios.post('http://localhost:4000/api/output/save', {
                                email: localStorage.getItem("email"),
                                imagePath: imagePath,
                                licensePlates: newPlateText,
                                timeStamp: new Date().toISOString()
                            });
                        }
                    }
                }
            }
            setOutput(plates)
        } catch (error) {
            console.error('Error uploading video:', error);
        }
    };

    return (
        <div className="input-container" onDrop={handleDrop} onDragOver={(e) => e.preventDefault()}>

            <div className="box">
                <h2 className='Video'>Video Analysis</h2>
                {!video ? (
                    <div className="upload-box">
                        <img src="src/assets/upload_icon.png" alt="Upload Icon" className="upload-icon" />
                        <p>Drag and drop a video or <span className="browse" onClick={() => document.getElementById('fileInput').click()}>browse</span></p>
                        <p className="file-info">File size can be up to 1GB</p>
                        <input type="file" id="fileInput" style={{ display: 'none' }} onChange={handleFileChange} />
                    </div>
                ) : (
                    <>
                        <div className="video-preview">
                            <video src={video} ></video>
                        </div>
                        <button onClick={clickButton}>Submit</button>
                    </>
                )}
            </div>
            <div className="output">
                <h3>Detected License Plates:</h3>
                {output.length > 0 ? (
                    <div>
                        <div className="image-gallery">
                            {output.map((plate, index) => (
                                <div key={index}>
                                    <strong>Plate {index + 1}: </strong>{plate}
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <p>No plates detected yet</p>
                )}
            </div>
        </div>
    );
}

export default Input;
