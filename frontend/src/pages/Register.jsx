import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await authService.register(username, email, password);
            navigate('/login');
        } catch (err) {
            setError('Registration failed. Username or email might be taken.');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-dark-bg relative overflow-hidden">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10" />

            <div className="max-w-md w-full space-y-8 p-10 glass-panel rounded-2xl relative z-10 neon-border">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-white font-mono">
                        INITIATE SEQUENCE
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-400 font-mono">
                        Join the future of commerce
                    </p>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="rounded-md shadow-sm -space-y-px">
                        <div className="mb-4">
                            <input
                                type="text"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 placeholder-gray-500 text-white bg-dark-surface focus:outline-none focus:ring-neon-pink focus:border-neon-pink focus:z-10 sm:text-sm font-mono"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div className="mb-4">
                            <input
                                type="email"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 placeholder-gray-500 text-white bg-dark-surface focus:outline-none focus:ring-neon-pink focus:border-neon-pink focus:z-10 sm:text-sm font-mono"
                                placeholder="Email Address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <input
                                type="password"
                                required
                                className="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 placeholder-gray-500 text-white bg-dark-surface focus:outline-none focus:ring-neon-pink focus:border-neon-pink focus:z-10 sm:text-sm font-mono"
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
                            className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-md text-black bg-neon-pink hover:bg-neon-purple hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neon-pink transition-all duration-300 uppercase tracking-widest"
                        >
                            Create Account
                        </button>
                    </div>

                    <div className="text-center mt-4">
                        <Link to="/login" className="text-sm text-gray-400 hover:text-neon-blue font-mono">
                            Already have access? Login
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
