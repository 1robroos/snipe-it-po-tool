#!/usr/bin/env python3
"""
Debug script to check purchase costs
"""

import os
import sys
from dotenv import load_dotenv

sys.path.append('src')
from snipe_api import SnipeAPI

def debug_purchase_costs():
    """Debug purchase costs for all assets"""
    load_dotenv()
    
    api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
    
    print("🔍 Checking purchase costs for all assets...")
    print("=" * 60)
    
    assets = api.get_assets()
    
    for asset in assets['rows']:
        try:
            asset_detail = api.get_asset(asset['id'])
            
            # Get supplier info
            supplier_info = asset_detail.get('supplier', {})
            supplier_name = supplier_info.get('name', 'No Supplier') if supplier_info else 'No Supplier'
            
            # Get purchase cost
            purchase_cost = asset_detail.get('purchase_cost', {})
            if isinstance(purchase_cost, dict):
                amount = purchase_cost.get('amount', 0)
                if isinstance(amount, str):
                    amount = amount.replace(',', '')
                cost = float(amount) if amount else 0
                currency = purchase_cost.get('currency', 'USD')
            else:
                if isinstance(purchase_cost, str):
                    purchase_cost = purchase_cost.replace(',', '')
                cost = float(purchase_cost) if purchase_cost else 0
                currency = 'USD'
            
            print(f"📦 {asset.get('name', 'Unknown')}")
            print(f"   Model: {asset.get('model', {}).get('name', 'Unknown')}")
            print(f"   Supplier: {supplier_name}")
            print(f"   Purchase Cost: {currency} ${cost:.2f}")
            
            if cost == 0:
                print(f"   ⚠️  WARNING: No purchase cost set!")
            
            print()
            
        except Exception as e:
            print(f"❌ Error getting details for {asset.get('name', 'Unknown')}: {e}")
            print()

if __name__ == "__main__":
    debug_purchase_costs()
