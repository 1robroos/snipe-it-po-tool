#!/usr/bin/env python3
import os
import sys
sys.path.append('src')
from snipe_api import SnipeAPI

# Load environment variables manually
with open('.env', 'r') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'), False)
assets = api.get_assets(limit=500)

# Look for the specific assets
target_assets = ['D0077', 'SW2592', 'SK2690']

for asset in assets['rows']:
    asset_tag = asset.get('asset_tag', '')
    if asset_tag in target_assets:
        print(f"\n=== Asset {asset_tag} ===")
        print(f"Name: {asset.get('name', 'Unknown')}")
        print(f"Purchase Cost Raw: {asset.get('purchase_cost')}")
        print(f"Purchase Cost Type: {type(asset.get('purchase_cost'))}")
        
        # Get detailed asset info
        try:
            detailed = api.get_asset(asset['id'])
            print(f"Detailed Purchase Cost: {detailed.get('purchase_cost')}")
            print(f"Detailed Purchase Cost Type: {type(detailed.get('purchase_cost'))}")
        except Exception as e:
            print(f"Error getting detailed info: {e}")
