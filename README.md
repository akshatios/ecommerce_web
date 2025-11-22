# E-commerce API - FastAPI + React + MongoDB

A complete e-commerce application with user authentication, product management, and order processing.

## 🚀 Features

- **User Authentication** (Register, Login, JWT)
- **Product Management** (CRUD operations)
- **Order Management** (Create, View orders)
- **MongoDB Integration**
- **RESTful API** with FastAPI
- **Modern React Frontend** with Tailwind CSS

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **JWT** - Authentication
- **Bcrypt** - Password hashing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI and secret key

# Run backend
uvicorn app.main:app --reload
```

Backend will run on: `http://localhost:8000`

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Run frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

## 🌐 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user

### Products
- `GET /products` - Get all products
- `POST /products` - Create product (auth required)
- `GET /products/{id}` - Get product by ID
- `PUT /products/{id}` - Update product (auth required)
- `DELETE /products/{id}` - Delete product (auth required)

### Orders
- `POST /orders` - Create order (auth required)
- `GET /orders` - Get user orders (auth required)

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy
- **Frontend**: Vercel (Free)
- **Backend**: Render.com (Free)
- **Database**: MongoDB Atlas (Free)

## 📝 Environment Variables

### Backend (.env)
```
MONGO_URI=mongodb://localhost:27017/ecommerce_db
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
```

## 🔒 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS enabled for frontend
- Environment variables for sensitive data

## 📄 License

MIT License - feel free to use this project for learning or production!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ using FastAPI and React
