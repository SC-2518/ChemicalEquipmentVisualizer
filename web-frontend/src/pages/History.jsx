import React, { useEffect, useState } from 'react';
import api from '../api';
import { FileText, Download, Calendar, Database, Activity } from 'lucide-react';

const History = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('history/')
            .then(res => {
                setData(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    const downloadReport = (id) => {
        window.open(`http://localhost:8000/api/report/${id}/`, '_blank');
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white uppercase tracking-wider">Dataset History</h1>
                    <p className="text-slate-400 text-sm">Review and download reports for your past uploads.</p>
                </div>
            </div>

            <div className="glass-card overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-slate-800/50 text-slate-300 text-xs uppercase tracking-widest border-b border-white/5">
                                <th className="px-6 py-4 font-semibold">Filename</th>
                                <th className="px-6 py-4 font-semibold">Upload Date</th>
                                <th className="px-6 py-4 font-semibold">Records</th>
                                <th className="px-6 py-4 font-semibold">Avg Flow</th>
                                <th className="px-6 py-4 font-semibold text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {data.map((item) => (
                                <tr key={item.id} className="hover:bg-white/5 transition-colors group">
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 bg-primary-500/10 rounded-lg text-primary-400">
                                                <FileText size={18} />
                                            </div>
                                            <span className="text-sm font-medium text-slate-200">{item.filename}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2 text-slate-400 text-sm">
                                            <Calendar size={14} />
                                            {new Date(item.upload_date).toLocaleDateString()}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2 text-slate-400 text-sm">
                                            <Database size={14} />
                                            {item.total_records}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2 text-slate-400 text-sm">
                                            <Activity size={14} />
                                            {item.avg_flowrate.toFixed(1)}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <button
                                            onClick={() => downloadReport(item.id)}
                                            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary-500/10 text-primary-400 hover:bg-primary-500 hover:text-white transition-all text-xs font-semibold"
                                        >
                                            <Download size={14} />
                                            PDF Report
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {data.length === 0 && (
                                <tr>
                                    <td colSpan="5" className="px-6 py-12 text-center text-slate-500">
                                        No historical data found.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default History;
