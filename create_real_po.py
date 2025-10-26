#!/usr/bin/env python3
"""
Create purchase order with real Snipe-IT assets
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('src')

from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator

def create_purchase_order_from_snipeit():
    """Create PO with real assets from Snipe-IT"""
    load_dotenv()
    
    api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
    
    print("🔍 Fetching data from Snipe-IT...")
    
    # Get assets and suppliers
    assets = api.get_assets()
    suppliers = api.get_suppliers()
    
    print(f"   Found {assets['total']} assets")
    print(f"   Found {suppliers['total']} suppliers")
    
    # Use first supplier
    supplier = suppliers['rows'][0] if suppliers['rows'] else {'name': 'Default Supplier'}
    
    # Create PO data
    po_data = {
        'po_number': f"PO-REAL-{datetime.now().strftime('%Y%m%d-%H%M')}",
        'supplier_name': supplier['name'],
        'created_at': datetime.now().strftime('%B %d, %Y'),
        'status': 'draft',
        'items': [],
        'total_amount': 0
    }
    
    # Add assets as items (simulate pricing)
    total = 0
    for i, asset in enumerate(assets['rows'][:5]):  # Take first 5 assets
        # Simulate pricing based on asset type
        price = 299.99 if 'pc' in asset.get('name', '').lower() else 149.99
        quantity = 1
        
        po_data['items'].append({
            'asset_name': asset.get('name', 'Unknown Asset'),
            'model': asset.get('model', {}).get('name', 'Unknown Model'),
            'quantity': quantity,
            'unit_price': price,
            'total_price': price * quantity
        })
        total += price * quantity
    
    po_data['total_amount'] = total
    
    print(f"\n📋 Creating Purchase Order:")
    print(f"   PO Number: {po_data['po_number']}")
    print(f"   Supplier: {po_data['supplier_name']}")
    print(f"   Items: {len(po_data['items'])}")
    print(f"   Total: ${total:.2f}")
    
    # Generate PDF
    print(f"\n📄 Generating PDF...")
    pdf_gen = PDFGenerator()
    output_path = f"real_{po_data['po_number']}.pdf"
    
    # Convert items to expected format for PDF generator
    formatted_items = []
    for item in po_data['items']:
        formatted_items.append((
            0,  # id
            0,  # po_id
            0,  # asset_id
            f"{item['asset_name']} - {item['model']}",  # asset_name
            item['quantity'],  # quantity
            item['unit_price']  # unit_price
        ))
    
    po_data_for_pdf = {
        'po_number': po_data['po_number'],
        'supplier_name': po_data['supplier_name'],
        'created_at': po_data['created_at'],
        'status': po_data['status'],
        'items': formatted_items,
        'total_amount': po_data['total_amount']
    }
    
    pdf_path = pdf_gen.generate_purchase_order_pdf(po_data_for_pdf, output_path)
    
    if os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        print(f"✅ PDF generated successfully!")
        print(f"   📁 File: {pdf_path}")
        print(f"   📊 Size: {file_size:,} bytes")
        
        print(f"\n📋 Purchase Order Details:")
        for item in po_data['items']:
            print(f"   • {item['asset_name']} - {item['model']}")
            print(f"     ${item['unit_price']:.2f}")
        
        print(f"\n   💰 TOTAL: ${po_data['total_amount']:.2f}")
    else:
        print("❌ PDF generation failed")

if __name__ == "__main__":
    print("🛒 Real Snipe-IT Purchase Order Generator")
    print("=" * 50)
    create_purchase_order_from_snipeit()
