import React from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCart, User, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useAuth();

    return (
        <nav className="fixed top-0 w-full z-50 glass-panel border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <Link to="/" className="text-2xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-neon-pink to-neon-blue hover:scale-105 transition-transform">
                        CYBERSTORE
                    </Link>

                    <div className="flex items-center space-x-8">
                        <Link to="/products" className="text-gray-300 hover:text-neon-blue transition-colors font-mono">
                            CATALOG
                        </Link>

                        {user ? (
                            <>
                                <Link to="/cart" className="text-gray-300 hover:text-neon-green transition-colors">
                                    <ShoppingCart className="w-6 h-6" />
                                </Link>
                                <button onClick={logout} className="text-gray-300 hover:text-neon-pink transition-colors">
                                    <LogOut className="w-6 h-6" />
                                </button>
                            </>
                        ) : (
                            <div className="flex items-center space-x-4">
                                <Link to="/login" className="px-4 py-2 rounded bg-transparent border border-neon-purple text-neon-purple hover:bg-neon-purple hover:text-white transition-all duration-300 font-mono uppercase tracking-wider">
                                    Login
                                </Link>
                                <Link to="/register" className="px-4 py-2 rounded bg-neon-blue text-black font-bold hover:bg-neon-purple hover:text-white transition-all duration-300 font-mono uppercase tracking-wider">
                                    Register
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
