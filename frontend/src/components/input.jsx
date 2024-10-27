import React, { useState } from 'react';


function Input() {
    const [video, setVideo] = useState(null);

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (file && file.type.includes('video')) {
            const videoURL = URL.createObjectURL(file);
            setVideo(videoURL);

            const formData = new FormData();
            formData.append('video', file);

        try {
            const response = await fetch('http://localhost:5000/process-video', {
                method: 'POST',
                // headers: {
                //     'Content-Type': 'multipart/form-data',
                // },
                body: formData,
            });
            if (!response.ok) {
                throw new Error('Failed to login');
            }
    
            const data = await response.json();
            if (data===null){
                throw new Error('Failed ');
            }
            console.log("Success");
            
        } catch (error) {
            alert('Failed to upload video');
            console.error('Error', error);
            throw error;
        }
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
