from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, orders

app = FastAPI(
    title="E-commerce API",
    description="A complete e-commerce API built with FastAPI and MongoDB",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce API"}
