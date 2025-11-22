import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const authService = {
    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        const response = await api.post('/login', formData);
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }
        return response.data;
    },
    register: async (username, email, password) => {
        const response = await api.post('/register', { username, email, password });
        return response.data;
    },
    logout: () => {
        localStorage.removeItem('token');
    }
};

export const productService = {
    getAll: async () => {
        const response = await api.get('/products');
        return response.data;
    },
    getOne: async (id) => {
        const response = await api.get(`/products/${id}`);
        return response.data;
    },
    create: async (product) => {
        const response = await api.post('/products', product);
        return response.data;
    }
};

export const orderService = {
    create: async (items, total) => {
        const response = await api.post('/orders', { items, total_amount: total });
        return response.data;
    },
    getAll: async () => {
        const response = await api.get('/orders');
        return response.data;
    }
};

export default api;
