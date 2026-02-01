import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (!user) return null;

    return (
        <nav className="bg-gray-800 p-4 text-white">
            <div className="container mx-auto flex justify-between items-center">
                <div className="font-bold text-xl">Equipment Visualizer</div>
                <div className="space-x-4">
                    <Link to="/" className="hover:text-gray-300">Dashboard</Link>
                    <Link to="/upload" className="hover:text-gray-300">Upload</Link>
                    <Link to="/history" className="hover:text-gray-300">History</Link>
                    <button onClick={handleLogout} className="bg-red-500 px-3 py-1 rounded hover:bg-red-600">Logout</button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
