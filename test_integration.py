#!/usr/bin/env python3
"""
Test script for Snipe-IT integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from snipe_api import SnipeAPI

def test_connection():
    """Test connection to Snipe-IT"""
    load_dotenv()
    
    base_url = os.getenv('SNIPE_URL')
    api_token = os.getenv('SNIPE_TOKEN')
    
    print(f"🔗 Testing connection to: {base_url}")
    
    if api_token == 'your-api-token-here':
        print("❌ API token not configured!")
        print("Please:")
        print("1. Go to http://localhost:8000")
        print("2. Login to Snipe-IT")
        print("3. Go to Account Settings > API Keys")
        print("4. Generate a new API key")
        print("5. Update .env file with your token")
        return False
    
    try:
        api = SnipeAPI(base_url, api_token)
        
        # Test basic connection
        print("📋 Getting assets...")
        assets = api.get_assets(limit=5)
        
        print(f"✅ Connection successful!")
        print(f"   Total assets: {assets.get('total', 0)}")
        
        if assets.get('rows'):
            print("   Sample assets:")
            for asset in assets['rows'][:3]:
                print(f"   • {asset.get('name', 'N/A')} - {asset.get('model', {}).get('name', 'N/A')}")
        
        # Test suppliers
        print("\n🏢 Getting suppliers...")
        suppliers = api.get_suppliers()
        print(f"   Total suppliers: {suppliers.get('total', 0)}")
        
        if suppliers.get('rows'):
            print("   Sample suppliers:")
            for supplier in suppliers['rows'][:3]:
                print(f"   • {supplier.get('name', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Snipe-IT Integration Test")
    print("=" * 40)
    test_connection()
