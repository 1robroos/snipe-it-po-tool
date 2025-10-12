import requests
import os
from typing import Dict, List, Optional

class SnipeAPI:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get_assets(self, limit: int = 50, offset: int = 0) -> Dict:
        """Get assets from Snipe-IT"""
        url = f"{self.base_url}/api/v1/hardware"
        params = {'limit': limit, 'offset': offset}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_asset(self, asset_id: int) -> Dict:
        """Get single asset by ID"""
        url = f"{self.base_url}/api/v1/hardware/{asset_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_suppliers(self) -> Dict:
        """Get all suppliers"""
        url = f"{self.base_url}/api/v1/suppliers"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_supplier(self, supplier_id: int) -> Dict:
        """Get single supplier by ID"""
        url = f"{self.base_url}/api/v1/suppliers/{supplier_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
