#!/usr/bin/env python3
import os
import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Simple API call without dependencies
SNIPE_URL = input("Enter Snipe-IT URL: ").strip()
SNIPE_TOKEN = input("Enter API Token: ").strip()

headers = {
    'Authorization': f'Bearer {SNIPE_TOKEN}',
    'Accept': 'application/json'
}

# Get assets
response = requests.get(f"{SNIPE_URL}/api/v1/hardware?limit=500", headers=headers, verify=False)
assets = response.json()

# Find D3367
for asset in assets['rows']:
    if asset.get('asset_tag') == 'D3367':
        print(f"=== Asset D3367 ===")
        print(f"Name: {asset.get('name')}")
        print(f"Purchase Cost: {asset.get('purchase_cost')}")
        print(f"Purchase Cost Type: {type(asset.get('purchase_cost'))}")
        
        # Get detailed info
        detail_response = requests.get(f"{SNIPE_URL}/api/v1/hardware/{asset['id']}", headers=headers, verify=False)
        detail = detail_response.json()
        print(f"Detailed Purchase Cost: {detail.get('purchase_cost')}")
        print(f"Detailed Purchase Cost Type: {type(detail.get('purchase_cost'))}")
        break
else:
    print("Asset D3367 not found")
