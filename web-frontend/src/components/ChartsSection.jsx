import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: { color: '#94a3b8' } // slate-400
        },
        title: {
            display: false,
        },
    },
    scales: {
        y: {
            grid: { color: 'rgba(255, 255, 255, 0.1)' },
            ticks: { color: '#94a3b8' }
        },
        x: {
            grid: { display: false },
            ticks: { color: '#94a3b8' }
        }
    }
};

const ChartsSection = ({ data }) => {
    // Placeholder data if none provided
    const barData = {
        labels: ['Reactors', 'Heat Exchangers', 'Pumps', 'Columns', 'Tanks'],
        datasets: [
            {
                label: 'Equipment Count',
                data: [12, 19, 8, 15, 10],
                backgroundColor: 'rgba(14, 165, 233, 0.6)', // primary-500
                borderColor: '#0ea5e9',
                borderWidth: 1,
            },
        ],
    };

    const lineData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
            {
                label: 'Avg Pressure (PSI)',
                data: [120, 125, 118, 130, 128, 135],
                borderColor: '#8b5cf6', // secondary-500
                backgroundColor: 'rgba(139, 92, 246, 0.2)',
                fill: true,
                tension: 0.4,
            },
        ],
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass-card p-6 h-80">
                <h3 className="text-lg font-semibold text-white mb-4">Equipment Distribution</h3>
                <Bar options={chartOptions} data={barData} />
            </div>
            <div className="glass-card p-6 h-80">
                <h3 className="text-lg font-semibold text-white mb-4">Pressure Trends</h3>
                <Line options={chartOptions} data={lineData} />
            </div>
        </div>
    );
};

export default ChartsSection;
