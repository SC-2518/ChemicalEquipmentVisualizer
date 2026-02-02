import React, { useState } from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';
import { Lock, User, ArrowRight } from 'lucide-react';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        const success = await login(username, password);
        if (success) {
            navigate('/');
        } else {
            alert('Invalid credentials');
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            {/* Animated Background Blobs */}
            <div className="fixed inset-0 overflow-hidden -z-10">
                <div className="absolute top-1/4 -left-20 w-80 h-80 bg-primary-500/20 rounded-full blur-[100px] animate-pulse"></div>
                <div className="absolute bottom-1/4 -right-20 w-80 h-80 bg-secondary-500/20 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '1s' }}></div>
            </div>

            <div className="w-full max-w-md animate-slide-up">
                <div className="glass-card p-8 md:p-10 space-y-8">
                    <div className="text-center space-y-2">
                        <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-secondary-500 bg-clip-text text-transparent">
                            ChemVisualizer
                        </h1>
                        <p className="text-slate-400 text-sm">Industrial Equipment Parameter Monitoring</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-4">
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                                    <User size={18} />
                                </div>
                                <input
                                    type="text"
                                    placeholder="Username"
                                    value={username}
                                    onChange={e => setUsername(e.target.value)}
                                    className="glass-input w-full py-3 pl-10 pr-4 rounded-xl text-white placeholder-slate-500"
                                    required
                                />
                            </div>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                                    <Lock size={18} />
                                </div>
                                <input
                                    type="password"
                                    placeholder="Password"
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                    className="glass-input w-full py-3 pl-10 pr-4 rounded-xl text-white placeholder-slate-500"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full group py-3.5 px-4 bg-gradient-to-r from-primary-500 to-secondary-600 hover:from-primary-400 hover:to-secondary-500 text-white rounded-xl font-bold transition-all shadow-lg shadow-primary-500/25 flex items-center justify-center gap-2"
                        >
                            {isLoading ? 'Signing in...' : 'Sign In'}
                            {!isLoading && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
                        </button>
                    </form>

                    <div className="pt-4 text-center">
                        <p className="text-xs text-slate-500">
                            Default credentials: <span className="text-slate-300">admin / password123</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
