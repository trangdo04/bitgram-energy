import React, { useState } from 'react';

function Input() {
    const [video, setVideo] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.includes('video')) {
            const videoURL = URL.createObjectURL(file);
            setVideo(videoURL);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type.includes('video')) {
            const videoURL = URL.createObjectURL(file);
            setVideo(videoURL);
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
                <div className="video-preview">
                    <video src={video} controls style={{ width: '100%', height: '100%', objectFit: 'cover' }}></video>
                </div>
            )}
        </div>
    );
}

export default Input;
