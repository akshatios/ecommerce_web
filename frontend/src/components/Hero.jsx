import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Hero = () => {
    return (
        <div className="relative h-screen flex items-center justify-center overflow-hidden bg-dark-bg">
            {/* Background Elements */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-neon-purple/20 via-dark-bg to-dark-bg" />
            <div className="absolute top-0 left-0 w-full h-full bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />

            <div className="relative z-10 text-center px-4">
                <motion.h1
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className="text-7xl md:text-9xl font-black font-sans tracking-tighter text-white mb-6 mix-blend-overlay"
                >
                    FUTURE
                    <span className="block text-transparent bg-clip-text bg-gradient-to-r from-neon-pink via-neon-purple to-neon-blue animate-pulse-fast">
                        COMMERCE
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.3, duration: 0.8 }}
                    className="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto mb-12 font-mono"
                >
                    Experience the next generation of digital shopping. Aggressive style. Unmatched speed.
                </motion.p>

                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 0.6, duration: 0.5 }}
                >
                    <Link
                        to="/products"
                        className="group relative inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-200 bg-neon-blue font-mono uppercase tracking-widest hover:bg-neon-purple focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neon-blue"
                    >
                        <span className="absolute inset-0 w-full h-full -mt-1 rounded-lg opacity-30 bg-gradient-to-b from-transparent via-transparent to-black"></span>
                        <span className="relative">Start Shopping</span>
                    </Link>
                </motion.div>
            </div>
        </div>
    );
};

export default Hero;
