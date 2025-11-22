import React, { useEffect, useState } from 'react';
import Hero from '../components/Hero';
import ProductCard from '../components/ProductCard';
import { productService } from '../services/api';

const Home = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await productService.getAll();
                setProducts(data);
            } catch (error) {
                console.error("Failed to fetch products", error);
            }
        };
        fetchProducts();
    }, []);

    return (
        <div className="min-h-screen bg-dark-bg">
            <Hero />

            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                <div className="flex items-end justify-between mb-12">
                    <h2 className="text-4xl font-bold text-white font-sans tracking-tight">
                        LATEST <span className="text-neon-purple">DROPS</span>
                    </h2>
                    <div className="h-1 flex-1 mx-8 bg-white/10 rounded-full" />
                </div>

                <div className="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
                    {products.map((product) => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            </section>
        </div>
    );
};

export default Home;
