from fastapi import APIRouter
from app.routers import auth, products, orders

def register_routes(app):
    """
    Register all application routes
    
    Args:
        app: FastAPI application instance
    """
    
    # Include authentication routes
    app.include_router(
        auth.router,
        tags=['Authentication']
    )
    
    # Include product routes
    app.include_router(
        products.router,
        tags=['Products']
    )
    
    # Include order routes
    app.include_router(
        orders.router,
        tags=['Orders']
    )
    
    # Root endpoint
    @app.get("/", tags=['Root'])
    def root():
        """Welcome endpoint"""
        return {
            "message": "Welcome to the E-commerce API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    # Health check endpoint
    @app.get("/health", tags=['Health'])
    def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "E-commerce API"
        }
