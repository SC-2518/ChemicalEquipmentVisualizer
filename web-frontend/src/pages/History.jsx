import React, { useEffect, useState } from 'react';
import api from '../api';

const History = () => {
    const [data, setData] = useState([]);
    useEffect(() => {
        api.get('history/').then(res => setData(res.data)).catch(console.error);
    }, []);

    const downloadReport = (id) => {
        window.open(`http://localhost:8000/api/report/${id}/`, '_blank');
    };

    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-6">Upload History</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border shadow-sm rounded-lg overflow-hidden">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="py-3 px-4 border-b text-left">Filename</th>
                            <th className="py-3 px-4 border-b text-left">Upload Date</th>
                            <th className="py-3 px-4 border-b text-left">Total Records</th>
                            <th className="py-3 px-4 border-b text-left">Avg Flow</th>
                            <th className="py-3 px-4 border-b text-left">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map(item => (
                            <tr key={item.id} className="hover:bg-gray-50">
                                <td className="py-3 px-4 border-b">{item.filename}</td>
                                <td className="py-3 px-4 border-b">{new Date(item.upload_date).toLocaleString()}</td>
                                <td className="py-3 px-4 border-b">{item.total_records}</td>
                                <td className="py-3 px-4 border-b">{item.avg_flowrate.toFixed(2)}</td>
                                <td className="py-3 px-4 border-b">
                                    <button
                                        onClick={() => downloadReport(item.id)}
                                        className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                                    >
                                        PDF Report
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {data.length === 0 && (
                            <tr>
                                <td colSpan="5" className="py-4 text-center text-gray-500">No history available</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
export default History;
