import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, FileUp, History, Settings, Menu, Bell, User } from 'lucide-react';
import classNames from 'classnames';

const Layout = () => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: FileUp, label: 'Upload Data', path: '/upload' },
        { icon: History, label: 'History', path: '/history' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    return (
        <div className="flex h-screen overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 glass-card m-4 mr-0 flex flex-col hidden md:flex">
                <div className="p-6">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-secondary-500 bg-clip-text text-transparent">
                        ChemVisualizer
                    </h1>
                </div>

                <nav className="flex-1 px-4 space-y-2">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                classNames(
                                    'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group',
                                    isActive
                                        ? 'bg-primary-500/20 text-primary-400 shadow-lg shadow-primary-500/10'
                                        : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                                )
                            }
                        >
                            <item.icon size={20} />
                            <span className="font-medium">{item.label}</span>
                        </NavLink>
                    ))}
                </nav>

                <div className="p-4 border-t border-white/5">
                    <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/50">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center">
                            <span className="font-bold text-white">JD</span>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-white">John Doe</p>
                            <p className="text-xs text-slate-400">Engineer</p>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-screen overflow-hidden relative">
                {/* Header */}
                <header className="h-20 px-8 flex items-center justify-between z-10">
                    <div className="md:hidden">
                        <button className="p-2 text-slate-400 hover:text-white">
                            <Menu size={24} />
                        </button>
                    </div>

                    <div className="ml-auto flex items-center gap-4">
                        <button className="p-2 text-slate-400 hover:text-white relative">
                            <Bell size={20} />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500"></span>
                        </button>
                    </div>
                </header>

                {/* Page Content */}
                <div className="flex-1 overflow-y-auto px-8 pb-8 scrollbar-hide">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
