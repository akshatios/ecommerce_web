import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class APIRequest:
    """
    Helper class for making external API requests
    Supports GET, POST, PUT, DELETE methods
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30):
        """
        Initialize API Request helper
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def set_header(self, key: str, value: str):
        """Add or update a header"""
        self.headers[key] = value
    
    def set_auth_token(self, token: str, token_type: str = "Bearer"):
        """Set authorization token"""
        self.headers["Authorization"] = f"{token_type} {token}"
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
        
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers, **(headers or {})}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    url,
                    params=params,
                    headers=request_headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"GET request failed: {url} - {str(e)}")
            raise
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Additional headers
        
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers, **(headers or {})}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    data=data,
                    json=json_data,
                    headers=request_headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"POST request failed: {url} - {str(e)}")
            raise
    
    async def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make PUT request
        
        Args:
            endpoint: API endpoint
            json_data: JSON data
            headers: Additional headers
        
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers, **(headers or {})}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.put(
                    url,
                    json=json_data,
                    headers=request_headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"PUT request failed: {url} - {str(e)}")
            raise
    
    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make DELETE request
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
        
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.headers, **(headers or {})}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    url,
                    headers=request_headers
                )
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPError as e:
            logger.error(f"DELETE request failed: {url} - {str(e)}")
            raise

# Example usage:
# api = APIRequest(base_url="https://api.example.com")
# api.set_auth_token("your_token_here")
# result = await api.get("/users", params={"page": 1})
