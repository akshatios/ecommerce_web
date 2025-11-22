import React from 'react';
import { motion } from 'framer-motion';

const ProductCard = ({ product }) => {
    return (
        <motion.div
            whileHover={{ y: -10, scale: 1.02 }}
            className="relative group bg-dark-card border border-white/5 overflow-hidden rounded-xl"
        >
            <div className="aspect-w-1 aspect-h-1 w-full overflow-hidden bg-gray-800 xl:aspect-w-7 xl:aspect-h-8 relative">
                <div className="absolute inset-0 bg-gradient-to-t from-dark-bg to-transparent opacity-60 z-10" />
                <img
                    src={product.image_url || 'https://via.placeholder.com/400'} // Fallback image
                    alt={product.name}
                    className="h-full w-full object-cover object-center group-hover:opacity-75 transition-opacity duration-300"
                />
                <div className="absolute bottom-4 left-4 z-20">
                    <span className="inline-block px-2 py-1 text-xs font-bold text-black bg-neon-green font-mono mb-2">
                        {product.category}
                    </span>
                </div>
            </div>
            <div className="p-6 relative z-20">
                <h3 className="mt-1 text-xl font-bold text-white font-sans truncate">{product.name}</h3>
                <p className="mt-1 text-sm text-gray-400 line-clamp-2">{product.description}</p>
                <div className="mt-4 flex items-center justify-between">
                    <p className="text-2xl font-mono text-neon-blue">${product.price}</p>
                    <button className="px-4 py-2 bg-white/10 hover:bg-neon-pink text-white text-sm font-bold uppercase tracking-wider transition-colors duration-300">
                        Add to Cart
                    </button>
                </div>
            </div>

            {/* Hover Glow Effect */}
            <div className="absolute -inset-1 bg-gradient-to-r from-neon-pink to-neon-blue opacity-0 group-hover:opacity-20 blur transition duration-500 group-hover:duration-200" />
        </motion.div>
    );
};

export default ProductCard;
