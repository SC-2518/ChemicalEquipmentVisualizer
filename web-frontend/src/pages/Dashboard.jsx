import React, { useEffect, useState } from 'react';
import api from '../api';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const Dashboard = () => {
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        api.get('summary/')
            .then(res => setSummary(res.data))
            .catch(err => console.error("Failed to fetch summary", err));
    }, []);

    if (!summary) return <div className="p-8">Loading dashboard...</div>;

    const chartData = {
        labels: summary.type_distribution.map(d => d.equipment_type),
        datasets: [
            {
                label: 'Equipment Count by Type',
                data: summary.type_distribution.map(d => d.count),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
            },
        ],
    };

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">Dashboard - {summary.filename}</h1>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-white p-4 rounded shadow border">
                    <h3 className="text-gray-500 text-sm">Total Equipment</h3>
                    <p className="text-2xl font-bold">{summary.total_count}</p>
                </div>
                <div className="bg-white p-4 rounded shadow border">
                    <h3 className="text-gray-500 text-sm">Avg Flowrate</h3>
                    <p className="text-2xl font-bold">{summary.avg_flowrate.toFixed(1)}</p>
                </div>
                <div className="bg-white p-4 rounded shadow border">
                    <h3 className="text-gray-500 text-sm">Avg Pressure</h3>
                    <p className="text-2xl font-bold">{summary.avg_pressure.toFixed(1)}</p>
                </div>
                <div className="bg-white p-4 rounded shadow border">
                    <h3 className="text-gray-500 text-sm">Avg Temperature</h3>
                    <p className="text-2xl font-bold">{summary.avg_temperature.toFixed(1)}</p>
                </div>
            </div>

            <div className="bg-white p-6 rounded shadow border" style={{ height: '400px' }}>
                <h2 className="text-xl font-bold mb-4">Equipment Distribution</h2>
                <Bar options={{ maintainAspectRatio: false }} data={chartData} />
            </div>
        </div>
    );
};

export default Dashboard;
