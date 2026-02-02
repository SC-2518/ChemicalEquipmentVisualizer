import React, { useEffect, useState } from 'react';
import api from '../api';
import DashboardCard from '../components/DashboardCard';
import { Activity, Thermometer, Gauge, Database, BarChart3, LineChart, Cpu } from 'lucide-react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ScatterController,
} from 'chart.js';
import { Bar, Scatter, Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ScatterController
);

const Dashboard = () => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('summary/')
            .then(res => {
                setSummary(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch summary", err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (!summary) {
        return (
            <div className="text-center p-8">
                <h2 className="text-xl text-slate-400">No data available. Upload a CSV file to get started.</h2>
            </div>
        );
    }

    // Chart 1: Bar Chart (Count by Type)
    const barData = {
        labels: summary.type_distribution.map(d => d.equipment_type),
        datasets: [
            {
                label: 'Count',
                data: summary.type_distribution.map(d => d.count),
                backgroundColor: 'rgba(14, 165, 233, 0.6)',
                borderColor: '#0ea5e9',
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    };

    // Chart 2: Scatter Plot (Pressure vs Temp)
    const scatterData = {
        datasets: [
            {
                label: 'Pressure vs Temp',
                data: summary.raw_data_points.map(p => ({ x: p.temperature, y: p.pressure })),
                backgroundColor: 'rgba(139, 92, 246, 0.6)',
                borderColor: '#8b5cf6',
                pointRadius: 5,
                pointHoverRadius: 8,
            },
        ],
    };

    // Chart 3: Line Chart (Avg Metrics per Type)
    const metricsData = {
        labels: summary.type_distribution.map(d => d.equipment_type),
        datasets: [
            {
                label: 'Avg Flow',
                data: summary.type_distribution.map(d => d.avg_flow),
                borderColor: '#0ea5e9',
                backgroundColor: '#0ea5e9',
                tension: 0.3,
                borderWidth: 2,
            },
            {
                label: 'Avg Press',
                data: summary.type_distribution.map(d => d.avg_press),
                borderColor: '#8b5cf6',
                backgroundColor: '#8b5cf6',
                tension: 0.3,
                borderWidth: 2,
            }
        ]
    };

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: { color: '#94a3b8', boxWidth: 10, font: { size: 10 } }
            },
            tooltip: {
                backgroundColor: '#1e293b',
                titleColor: '#f8fafc',
                bodyColor: '#cbd5e1',
                padding: 10,
                cornerRadius: 8,
                borderColor: 'rgba(255,255,255,0.1)',
                borderWidth: 1
            }
        },
        scales: {
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', font: { size: 10 } } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } }
        }
    };

    const scatterOptions = {
        ...commonOptions,
        scales: {
            y: { ...commonOptions.scales.y, title: { display: true, text: 'Pressure (PSI)', color: '#64748b', font: { size: 10 } } },
            x: { ...commonOptions.scales.x, display: true, title: { display: true, text: 'Temp (°C)', color: '#64748b', font: { size: 10 } }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
        }
    };

    return (
        <div className="space-y-6 animate-fade-in pb-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white">Advanced Analytics Dashboard</h1>
                    <p className="text-slate-400 text-sm">Real-time equipment monitoring & cross-parameter analysis</p>
                </div>
                <div className="flex gap-2">
                    <span className="px-3 py-1 bg-primary-500/10 text-primary-400 rounded-full text-xs font-bold border border-primary-500/20">LIVE MONITORING</span>
                    <span className="px-3 py-1 bg-slate-800 text-slate-400 rounded-full text-xs font-bold border border-white/5">{summary.filename}</span>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <DashboardCard title="Total Equipment" value={summary.total_count} icon={Database} color="primary" />
                <DashboardCard title="Avg Flow Rate" value={`${summary.avg_flowrate.toFixed(1)} L/m`} icon={Activity} color="secondary" />
                <DashboardCard title="Avg Pressure" value={`${summary.avg_pressure.toFixed(1)} PSI`} icon={Gauge} color="emerald" />
                <DashboardCard title="Avg Temperature" value={`${summary.avg_temperature.toFixed(1)} °C`} icon={Thermometer} color="orange" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="glass-card p-6 h-[400px]">
                    <div className="flex items-center gap-2 mb-6">
                        <Cpu size={18} className="text-secondary-500" />
                        <h3 className="text-lg font-semibold text-white">Parameter Correlation (Pressure vs Temp)</h3>
                    </div>
                    <div className="h-[280px]">
                        <Scatter options={scatterOptions} data={scatterData} />
                    </div>
                </div>

                <div className="glass-card p-6 h-[400px]">
                    <div className="flex items-center gap-2 mb-6">
                        <LineChart size={18} className="text-primary-500" />
                        <h3 className="text-lg font-semibold text-white">Metrics Comparison by Equipment Type</h3>
                    </div>
                    <div className="h-[280px]">
                        <Line options={commonOptions} data={metricsData} />
                    </div>
                </div>

                <div className="glass-card p-6 h-[400px]">
                    <div className="flex items-center gap-2 mb-6">
                        <BarChart3 size={18} className="text-emerald-500" />
                        <h3 className="text-lg font-semibold text-white">Equipment Distribution</h3>
                    </div>
                    <div className="h-[280px]">
                        <Bar options={{ ...commonOptions, plugins: { ...commonOptions.plugins, legend: { display: false } } }} data={barData} />
                    </div>
                </div>

                <div className="glass-card p-6 h-[400px] flex flex-col">
                    <h3 className="text-lg font-semibold text-white mb-4">Statistical Breakdown</h3>
                    <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                        {summary.type_distribution.map((type, i) => (
                            <div key={i} className="p-4 rounded-xl bg-slate-900/40 border border-white/5 space-y-3 hover:bg-slate-900/60 transition-colors">
                                <div className="flex justify-between items-center">
                                    <span className="font-bold text-primary-400 tracking-wider uppercase text-[10px]">{type.equipment_type}</span>
                                    <span className="px-2 py-0.5 rounded-md bg-white/5 text-[10px] text-slate-400 font-medium">{type.count} units</span>
                                </div>
                                <div className="grid grid-cols-3 gap-2">
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-500 uppercase">Avg Flow</p>
                                        <p className="text-sm font-bold text-white">{type.avg_flow.toFixed(1)}</p>
                                    </div>
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-500 uppercase">Avg Press</p>
                                        <p className="text-sm font-bold text-white">{type.avg_press.toFixed(1)}</p>
                                    </div>
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-500 uppercase">Avg Temp</p>
                                        <p className="text-sm font-bold text-white">{type.avg_temp.toFixed(1)}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
