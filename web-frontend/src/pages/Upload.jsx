import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        try {
            await api.post('upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            navigate('/');
        } catch (err) {
            alert('Upload failed: ' + (err.response?.data?.error || err.message));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-lg mx-auto bg-white rounded shadow mt-10">
            <h2 className="text-2xl font-bold mb-4">Upload Dataset (CSV)</h2>
            <form onSubmit={handleUpload} className="flex flex-col gap-4">
                <input
                    type="file"
                    onChange={e => setFile(e.target.files[0])}
                    accept=".csv"
                    className="border p-2 rounded"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="bg-green-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
                >
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </form>
            <div className="mt-4 text-sm text-gray-500">
                <p>Expected Columns: Equipment Name, Type, Flowrate, Pressure, Temperature</p>
            </div>
        </div>
    );
};
export default Upload;
