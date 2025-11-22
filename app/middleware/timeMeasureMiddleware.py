from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimeMeasureMiddleware(BaseHTTPMiddleware):
    """
    Middleware to measure request processing time
    Logs the time taken for each request
    """
    
    def __init__(self, app, log_slow_requests: bool = True, slow_threshold: float = 1.0):
        super().__init__(app)
        self.log_slow_requests = log_slow_requests
        self.slow_threshold = slow_threshold  # seconds
    
    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        
        # Log request details
        log_message = (
            f"{request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Time: {process_time:.4f}s"
        )
        
        # Log slow requests with warning
        if self.log_slow_requests and process_time > self.slow_threshold:
            logger.warning(f"⚠️  SLOW REQUEST: {log_message}")
        else:
            logger.info(log_message)
        
        return response

# Example usage in main.py:
# from app.middleware.timeMeasureMiddleware import TimeMeasureMiddleware
# app.add_middleware(TimeMeasureMiddleware, log_slow_requests=True, slow_threshold=1.0)
