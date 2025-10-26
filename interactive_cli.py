#!/usr/bin/env python3
"""
Interactive command-line interface for custom Purchase Order creation
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('src')
from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator

def interactive_po_creation():
    """Interactive PO creation via command line"""
    load_dotenv()
    
    print("🛒 Interactive Purchase Order Creator")
    print("=" * 50)
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
        
        # Get suppliers
        print("🏢 Loading suppliers...")
        suppliers = api.get_suppliers()
        
        if not suppliers['rows']:
            print("❌ No suppliers found!")
            return
        
        print("\nAvailable suppliers:")
        for i, supplier in enumerate(suppliers['rows'], 1):
            print(f"  {i}. {supplier['name']}")
        
        # Select supplier
        while True:
            try:
                choice = int(input(f"\nSelect supplier (1-{len(suppliers['rows'])}): ")) - 1
                if 0 <= choice < len(suppliers['rows']):
                    selected_supplier = suppliers['rows'][choice]
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
        
        print(f"\n✅ Selected supplier: {selected_supplier['name']}")
        
        # Get assets for this supplier
        print("\n📦 Loading assets...")
        assets = api.get_assets()
        supplier_assets = []
        
        for asset in assets['rows']:
            try:
                asset_detail = api.get_asset(asset['id'])
                asset_supplier = asset_detail.get('supplier', {})
                
                if asset_supplier and asset_supplier.get('id') == selected_supplier['id']:
                    supplier_assets.append({
                        'id': asset['id'],
                        'name': asset.get('name', 'Unknown'),
                        'model': asset.get('model', {}).get('name', 'Unknown Model'),
                        'detail': asset_detail
                    })
            except:
                continue
        
        if not supplier_assets:
            print(f"❌ No assets found for supplier {selected_supplier['name']}")
            return
        
        print(f"\nAssets from {selected_supplier['name']}:")
        for i, asset in enumerate(supplier_assets, 1):
            print(f"  {i}. {asset['name']} - {asset['model']}")
        
        # Select assets
        selected_assets = []
        print(f"\nSelect assets (enter numbers separated by commas, e.g., 1,2,3):")
        print("Or enter 'all' to select all assets")
        
        selection = input("Your choice: ").strip()
        
        if selection.lower() == 'all':
            selected_assets = supplier_assets.copy()
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                for idx in indices:
                    if 0 <= idx < len(supplier_assets):
                        selected_assets.append(supplier_assets[idx])
            except ValueError:
                print("Invalid selection!")
                return
        
        if not selected_assets:
            print("❌ No assets selected!")
            return
        
        print(f"\n✅ Selected {len(selected_assets)} assets")
        
        # Get pricing for each asset
        po_items = []
        total = 0
        
        for asset in selected_assets:
            print(f"\n📋 Asset: {asset['name']} - {asset['model']}")
            
            # Get purchase cost from Snipe-IT
            purchase_cost = asset['detail'].get('purchase_cost', {})
            if isinstance(purchase_cost, dict):
                amount = purchase_cost.get('amount', 0)
                if isinstance(amount, str):
                    amount = amount.replace(',', '')
                price = float(amount) if amount else 0
            else:
                if isinstance(purchase_cost, str):
                    purchase_cost = purchase_cost.replace(',', '')
                price = float(purchase_cost) if purchase_cost else 0
            
            print(f"  Purchase Cost: ${price:.2f}")
            
            # Get quantity
            while True:
                try:
                    quantity = int(input("  Quantity (default 1): ") or "1")
                    if quantity > 0:
                        break
                    else:
                        print("  Quantity must be positive!")
                except ValueError:
                    print("  Please enter a valid number!")
            
            po_items.append((
                0, 0, asset['id'],
                f"{asset['name']} - {asset['model']}",
                quantity, price
            ))
            total += price * quantity
            
            print(f"  ✅ Added: {quantity}x ${price:.2f} = ${quantity * price:.2f}")
        
        # Create PO
        po_number = f"PO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        po_data = {
            'po_number': po_number,
            'supplier_name': selected_supplier['name'],
            'created_at': datetime.now().strftime('%B %d, %Y'),
            'status': 'draft',
            'items': po_items,
            'total_amount': total
        }
        
        print(f"\n📋 Purchase Order Summary:")
        print(f"   PO Number: {po_number}")
        print(f"   Supplier: {selected_supplier['name']}")
        print(f"   Items: {len(po_items)}")
        print(f"   Total: ${total:.2f}")
        
        # Confirm creation
        confirm = input(f"\nCreate purchase order? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Purchase order cancelled")
            return
        
        # Generate PDF
        print(f"\n📄 Generating PDF...")
        pdf_gen = PDFGenerator()
        output_path = f"interactive_{po_number}.pdf"
        
        pdf_path = pdf_gen.generate_purchase_order_pdf(po_data, output_path)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ Purchase Order created successfully!")
            print(f"   📁 File: {pdf_path}")
            print(f"   📊 Size: {file_size:,} bytes")
        else:
            print("❌ Error generating PDF")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    interactive_po_creation()
