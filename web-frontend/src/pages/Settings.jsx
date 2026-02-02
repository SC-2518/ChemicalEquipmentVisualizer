import React from 'react';
import { User, Shield, Bell, Globe, Moon } from 'lucide-react';

const Settings = () => {
    return (
        <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
            <div>
                <h1 className="text-2xl font-bold text-white">System Settings</h1>
                <p className="text-slate-400 text-sm">Manage your profile, account security, and dashboard preferences.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Sidebar-like menu for settings */}
                <div className="md:col-span-1 space-y-2">
                    {[
                        { icon: User, label: 'Profile', active: true },
                        { icon: Shield, label: 'Security', active: false },
                        { icon: Bell, label: 'Notifications', active: false },
                        { icon: Globe, label: 'API Configuration', active: false },
                    ].map((item, i) => (
                        <button
                            key={i}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${item.active ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20' : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
                                }`}
                        >
                            <item.icon size={18} />
                            <span className="font-medium">{item.label}</span>
                        </button>
                    ))}
                </div>

                {/* Settings Form */}
                <div className="md:col-span-2 space-y-6">
                    <div className="glass-card p-6 space-y-6">
                        <div className="flex items-center gap-4">
                            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center text-3xl font-bold text-white shadow-lg">
                                JD
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-white">John Doe</h3>
                                <p className="text-slate-400">Senior Industrial Engineer</p>
                            </div>
                            <button className="ml-auto px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-medium transition-colors border border-white/5">
                                Change Avatar
                            </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-white/5">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-400">Full Name</label>
                                <input type="text" defaultValue="John Doe" className="glass-input w-full" />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-400">Email Address</label>
                                <input type="email" defaultValue="j.doe@company.com" className="glass-input w-full" />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-400">Department</label>
                                <input type="text" defaultValue="Engineering" className="glass-input w-full" />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-slate-400">Role</label>
                                <input type="text" defaultValue="Administrator" className="glass-input w-full" disabled />
                            </div>
                        </div>
                    </div>

                    <div className="glass-card p-6 space-y-4">
                        <h3 className="text-lg font-bold text-white border-b border-white/5 pb-2">Appearance</h3>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <Moon size={20} className="text-slate-400" />
                                <div>
                                    <p className="text-white font-medium">Dark Mode</p>
                                    <p className="text-xs text-slate-500">Currently active on the entire dashboard.</p>
                                </div>
                            </div>
                            <div className="w-12 h-6 bg-primary-600 rounded-full relative">
                                <div className="absolute top-1 right-1 w-4 h-4 bg-white rounded-full"></div>
                            </div>
                        </div>
                    </div>

                    <div className="flex justify-end gap-3">
                        <button className="px-6 py-2.5 rounded-xl border border-white/10 text-slate-300 hover:bg-white/5 transition-all">Cancel</button>
                        <button className="px-6 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white font-bold transition-all shadow-lg shadow-primary-500/20">Save Changes</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
