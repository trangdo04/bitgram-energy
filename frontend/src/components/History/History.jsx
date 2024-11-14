import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './History.css'; // Import file CSS

const History = () => {
    const email = localStorage.getItem("email");
    const [history, setHistory] = useState([]);
    const [pagination, setPagination] = useState({});
    const itemsPerPage = 3;

    const fetchHistory = async () => {
        try {
            const response = await axios.post("http://localhost:4000/api/output/history", { email });
            if (response.status === 200) {
                setHistory(response.data.history);
                console.log(response.data.history);
            }
        } catch (error) {
            console.error("Error fetching history:", error);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    // Nhóm các mục theo ngày
    const groupByDate = (data) => {
        return data.reduce((acc, item) => {
            const date = new Date(item.timeStamp).toLocaleDateString();
            if (!acc[date]) {
                acc[date] = [];
            }
            acc[date].push(item);
            return acc;
        }, {});
    };

    const groupedHistory = groupByDate(history);

    const handlePageChange = (date, direction) => {
        setPagination((prev) => ({
            ...prev,
            [date]: Math.max(0, (prev[date] || 0) + direction),
        }));
    };

    const renderBoxes = (items) => {
        return (
            <div className="box-container">
                {items.map((item) => (
                    <div key={item._id} className="history-box">
                        <div className="image-container">
                            <img
                                src={`http://localhost:5000/${item.imagePath}`}  // URL ảnh
                                alt="Processed Frame"
                                className="processed-image"
                            />
                        </div>
                        <p><strong>License Plates: </strong></p>{item.licensePlates}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="history-container">
            {Object.keys(groupedHistory).map((date) => {
                const items = groupedHistory[date];
                const totalPages = Math.ceil(items.length / itemsPerPage);
                const currentPage = pagination[date] || 0;

                return (
                    <div key={date} className="history-date-section">
                        <h2>Date: {date}</h2>
                        {renderBoxes(items.slice(currentPage * itemsPerPage, (currentPage + 1) * itemsPerPage))}
                        <div className="pagination">
                            <button
                                onClick={() => handlePageChange(date, -1)}
                                disabled={currentPage === 0}
                            >
                                Before
                            </button>
                            <span>
                                Page {currentPage + 1} of {totalPages}
                            </span>
                            <button
                                onClick={() => handlePageChange(date, 1)}
                                disabled={currentPage >= totalPages - 1}
                            >
                                After
                            </button>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default History;
