import React, { useState } from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await login(username, password);
        if (success) navigate('/');
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-80">
                <h2 className="text-xl font-bold mb-4">Login</h2>
                <input
                    type="text" placeholder="Username"
                    value={username} onChange={e => setUsername(e.target.value)}
                    className="w-full mb-3 p-2 border rounded"
                />
                <input
                    type="password" placeholder="Password"
                    value={password} onChange={e => setPassword(e.target.value)}
                    className="w-full mb-4 p-2 border rounded"
                />
                <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">Login</button>
            </form>
        </div>
    );
};

export default Login;
