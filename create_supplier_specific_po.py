#!/usr/bin/env python3
"""
Create purchase orders grouped by supplier
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('src')

from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator

def create_supplier_specific_pos():
    """Create separate POs per supplier with their assets"""
    load_dotenv()
    
    api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
    
    print("🔍 Fetching detailed asset data...")
    
    # Get all assets with full details
    assets = api.get_assets()
    suppliers = api.get_suppliers()
    
    # Group assets by supplier
    supplier_assets = {}
    
    for asset in assets['rows']:
        # Get detailed asset info to find supplier
        try:
            asset_detail = api.get_asset(asset['id'])
            supplier_info = asset_detail.get('supplier', {})
            supplier_name = supplier_info.get('name') if supplier_info else 'No Supplier'
            
            if supplier_name not in supplier_assets:
                supplier_assets[supplier_name] = []
            
            supplier_assets[supplier_name].append({
                'name': asset.get('name', 'Unknown'),
                'model': asset.get('model', {}).get('name', 'Unknown Model'),
                'id': asset['id']
            })
            
        except Exception as e:
            print(f"   Warning: Could not get details for asset {asset.get('name', 'Unknown')}: {e}")
            # Add to 'No Supplier' group if error
            if 'No Supplier' not in supplier_assets:
                supplier_assets['No Supplier'] = []
            
            supplier_assets['No Supplier'].append({
                'name': asset.get('name', 'Unknown'),
                'model': asset.get('model', {}).get('name', 'Unknown Model'),
                'id': asset['id']
            })
    
    print(f"\n📊 Assets grouped by supplier:")
    for supplier, assets_list in supplier_assets.items():
        print(f"   {supplier}: {len(assets_list)} assets")
        for asset in assets_list:
            print(f"     • {asset['name']} - {asset['model']}")
    
    # Create PO for each supplier that has assets
    generated_pos = []
    
    for supplier_name, assets_list in supplier_assets.items():
        if not assets_list:
            continue
            
        print(f"\n📋 Creating PO for {supplier_name}...")
        
        po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Create PO data
        po_data = {
            'po_number': po_number,
            'supplier_name': supplier_name,
            'created_at': datetime.now().strftime('%B %d, %Y'),
            'status': 'draft',
            'items': [],
            'total_amount': 0
        }
        
        # Add assets as items
        total = 0
        formatted_items = []
        
        for asset in assets_list:
            # Get purchase cost from Snipe-IT
            try:
                asset_detail = api.get_asset(asset['id'])
                purchase_cost = asset_detail.get('purchase_cost', {})
                if isinstance(purchase_cost, dict):
                    amount = purchase_cost.get('amount', 0)
                    if isinstance(amount, str):
                        amount = amount.replace(',', '')
                    price = float(amount) if amount else 0
                else:
                    if isinstance(purchase_cost, str):
                        purchase_cost = purchase_cost.replace(',', '')
                    price = float(purchase_cost) if purchase_cost else 0
            except:
                price = 0  # Fallback if can't get purchase cost
            
            quantity = 1
            
            formatted_items.append((
                0,  # id
                0,  # po_id
                asset['id'],  # asset_id
                f"{asset['name']} - {asset['model']}",  # asset_name
                quantity,  # quantity
                price  # unit_price
            ))
            total += price * quantity
        
        po_data['items'] = formatted_items
        po_data['total_amount'] = total
        
        # Generate PDF
        print(f"   📄 Generating PDF for {supplier_name}...")
        pdf_gen = PDFGenerator()
        output_path = f"supplier_{po_number}.pdf"
        
        pdf_path = pdf_gen.generate_purchase_order_pdf(po_data, output_path)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"   ✅ PDF: {pdf_path} ({file_size:,} bytes)")
            print(f"   💰 Total: ${total:.2f}")
            generated_pos.append((supplier_name, pdf_path, total))
        else:
            print(f"   ❌ Failed to generate PDF for {supplier_name}")
    
    print(f"\n🎉 Generated {len(generated_pos)} purchase orders:")
    total_all = 0
    for supplier, pdf_path, amount in generated_pos:
        print(f"   • {supplier}: {pdf_path} - ${amount:.2f}")
        total_all += amount
    
    print(f"\n💰 GRAND TOTAL: ${total_all:.2f}")

if __name__ == "__main__":
    print("🏢 Supplier-Specific Purchase Order Generator")
    print("=" * 55)
    create_supplier_specific_pos()
