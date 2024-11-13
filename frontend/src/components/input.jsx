import React, { useState } from 'react';
import axios from 'axios';

function Input() {
    const [video, setVideo] = useState(null);
    const [input, setInput] = useState(null);
    const [imageUrls, setImageUrls] = useState([]); // Renamed to imageUrls for clarity
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

            if (response.status === 200) {
                console.log(response.data.image_urls);
                setImageUrls(response.data.image_urls);
                recognizeLP(response.data.image_urls);
            }
        } catch (error) {
            console.error('Error uploading video:', error);
        }
    };

    const recognizeLP = async (imageUrls) => {
        try {
            const plates = [];
            for (const imageUrl of imageUrls) {
                const imageResponse = await axios.get(`http://localhost:5000/output_frames/${imageUrl}`, {
                    responseType: 'blob',
                });

                const formData = new FormData();
                formData.append('file', imageResponse.data, 'frame.jpg');

                const lpResponse = await axios.post('http://localhost:5001/lp_recognition', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                if (lpResponse.status === 200) {
                    plates.push({ imageUrl, data: lpResponse.data.plates }); // Save recognition results
                    console.log(lpResponse.data.plates)
                    await axios.post('http://localhost:4000/api/output/save', {
                        noHelmet: imageUrl,
                        licensePlates: lpResponse.data.plates,
                        timeStamp: new Date().toISOString()
                    });
                }
            }

            setOutput(plates); // Update output with license plate recognition results
        } catch (error) {
            console.error('Error recognizing LP:', error);
        }
    };

    return (
        <div className="input-container" onDrop={handleDrop} onDragOver={(e) => e.preventDefault()}>
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
                        <video src={video} controls style={{ width: '100%', height: '100%', objectFit: 'cover' }}></video>
                    </div>
                    <button onClick={clickButton}>Submit</button>
                </>
            )}
            <div className="output">
                {output.length > 0 ? (
                    <div>
                        <h3>Detected License Plates:</h3>
                        <div className="image-gallery">
                            {output.map((plateInfo, index) => (
                                <div key={index} className="image-item">
                                    <h4>Frame {index + 1}</h4>
                                    {plateInfo.data.map((plate, plateIndex) => (
                                        <p key={plateIndex}>
                                            <strong>Plate {plateIndex + 1} Text:</strong> {plate.text}
                                        </p>
                                    ))}
                                    <img src={`http://localhost:5000/output_frames/${plateInfo.imageUrl}`} alt={`Frame ${index + 1}`} style={{ width: '100%', height: 'auto' }} />
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
