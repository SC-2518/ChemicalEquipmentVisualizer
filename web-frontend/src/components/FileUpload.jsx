import React, { useState } from 'react';
import { Upload, FileType, X, CheckCircle } from 'lucide-react';
import classNames from 'classnames';

const FileUpload = ({ onUpload }) => {
    const [dragActive, setDragActive] = useState(false);
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = () => {
        if (!file) return;
        setUploading(true);

        // Simulate upload
        let p = 0;
        const interval = setInterval(() => {
            p += 10;
            setProgress(p);
            if (p >= 100) {
                clearInterval(interval);
                setUploading(false);
                if (onUpload) onUpload(file);
            }
        }, 200);
    };

    return (
        <div className="glass-card p-8 text-center">
            {!file ? (
                <div
                    className={classNames(
                        "border-2 border-dashed rounded-xl p-10 transition-all duration-200 cursor-pointer relative",
                        dragActive ? "border-primary-500 bg-primary-500/10" : "border-slate-600 hover:border-slate-500 hover:bg-slate-800/50"
                    )}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        type="file"
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={handleChange}
                        accept=".csv"
                    />
                    <div className="flex flex-col items-center gap-4">
                        <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center">
                            <Upload className="text-primary-500" size={32} />
                        </div>
                        <div>
                            <p className="text-lg font-medium text-white">Click to upload or drag and drop</p>
                            <p className="text-slate-400 mt-1">CSV files only (max 10MB)</p>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="bg-slate-800/50 rounded-xl p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                            <div className="p-3 bg-primary-500/20 rounded-lg">
                                <FileType className="text-primary-400" size={24} />
                            </div>
                            <div className="text-left">
                                <p className="font-medium text-white">{file.name}</p>
                                <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB</p>
                            </div>
                        </div>
                        <button
                            onClick={() => setFile(null)}
                            className="p-1 hover:bg-slate-700 rounded-full text-slate-400 hover:text-white"
                        >
                            <X size={20} />
                        </button>
                    </div>

                    {uploading ? (
                        <div className="w-full bg-slate-700 rounded-full h-2.5 mb-2 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2.5 rounded-full transition-all duration-300"
                                style={{ width: `${progress}%` }}
                            ></div>
                        </div>
                    ) : (
                        <button
                            onClick={handleUpload}
                            className="w-full py-3 px-4 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-400 hover:to-primary-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-primary-500/20"
                        >
                            Process Dataset
                        </button>
                    )}

                    {progress === 100 && (
                        <div className="mt-4 flex items-center justify-center gap-2 text-emerald-400">
                            <CheckCircle size={20} />
                            <span className="font-medium">Upload Complete!</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default FileUpload;
