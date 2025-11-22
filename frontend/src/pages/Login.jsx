import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(username, password);
            navigate('/');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-dark-bg relative overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10" />

            <div className="max-w-md w-full space-y-8 p-10 glass-panel rounded-2xl relative z-10 neon-border">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-white font-mono">
                        SYSTEM ACCESS
                    </h2>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div className="mb-4">
                            <input
                                type="text"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 placeholder-gray-500 text-white bg-dark-surface focus:outline-none focus:ring-neon-blue focus:border-neon-blue focus:z-10 sm:text-sm font-mono"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div>
                            <input
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 placeholder-gray-500 text-white bg-dark-surface focus:outline-none focus:ring-neon-blue focus:border-neon-blue focus:z-10 sm:text-sm font-mono"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="text-neon-pink text-sm text-center font-mono">{error}</div>
                    )}

                    <div>
                        <button
                            type="submit"
                            className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-md text-black bg-neon-blue hover:bg-neon-purple hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neon-blue transition-all duration-300 uppercase tracking-widest"
                        >
                            Enter System
                        </button>
                    </div>

                    <div className="text-center mt-4">
                        <Link to="/register" className="text-sm text-gray-400 hover:text-neon-blue font-mono">
                            New user? Create account
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
