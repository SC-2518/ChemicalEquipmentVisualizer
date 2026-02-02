import React from 'react';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';
import api from '../api';

const Upload = () => {
    const navigate = useNavigate();

    const handleUpload = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post('upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            // Redirect to dashboard after successful upload
            // Add a small delay for the user to see success state
            setTimeout(() => {
                navigate('/');
            }, 1000);
        } catch (error) {
            console.error("Upload failed", error);
            alert("Upload failed. Please try again.");
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-white">Upload Dataset</h1>
                <p className="text-slate-400 text-sm">Upload a new CSV file to update the dashboard metrics.</p>
            </div>

            <FileUpload onUpload={handleUpload} />

            <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Required Format</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left text-slate-400">
                        <thead className="text-xs text-slate-200 uppercase bg-slate-800/50">
                            <tr>
                                <th className="px-6 py-3">Equipment_ID</th>
                                <th className="px-6 py-3">Type</th>
                                <th className="px-6 py-3">Flowrate (L/m)</th>
                                <th className="px-6 py-3">Pressure (PSI)</th>
                                <th className="px-6 py-3">Temperature (°C)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr className="border-b border-slate-700">
                                <td className="px-6 py-4">EQ-001</td>
                                <td className="px-6 py-4">Reactor</td>
                                <td className="px-6 py-4">45.2</td>
                                <td className="px-6 py-4">120</td>
                                <td className="px-6 py-4">85</td>
                            </tr>
                            <tr className="border-b border-slate-700" >
                                <td className="px-6 py-4">EQ-002</td>
                                <td className="px-6 py-4">Pump</td>
                                <td className="px-6 py-4">22.1</td>
                                <td className="px-6 py-4">45</td>
                                <td className="px-6 py-4">30</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Upload;
