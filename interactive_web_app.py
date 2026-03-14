#!/usr/bin/env python3
"""
Interactive web interface for custom Purchase Order creation
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('src')
from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator
from po_counter import get_next_po_number

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def get_purchase_cost(asset_detail):
    """Extract purchase cost from asset detail - support multiple formats"""
    purchase_cost_raw = asset_detail.get('purchase_cost', 0)
    
    if isinstance(purchase_cost_raw, dict):
        # Format: {"amount": "150000", "currency": "EUR"}
        amount = purchase_cost_raw.get('amount', 0)
        if amount:
            try:
                return float(str(amount).replace(',', '')) / 100
            except (ValueError, TypeError):
                return 0
    elif isinstance(purchase_cost_raw, (int, float)):
        # Format: 150000 (already in cents)
        return float(purchase_cost_raw) / 100
    elif isinstance(purchase_cost_raw, str) and purchase_cost_raw:
        # Format: "150000" or "1500.00"
        try:
            value = float(purchase_cost_raw.replace(',', ''))
            # If value > 1000, assume it's in cents, otherwise euros
            return value / 100 if value > 1000 else value
        except (ValueError, TypeError):
            return 0
    
    return 0

@app.route('/')
def index():
    """Main page with asset selection"""
    load_dotenv()
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'), 
                      os.getenv('VERIFY_SSL', 'true').lower() == 'true')
        assets = api.get_assets(limit=500)
        suppliers = api.get_suppliers()
        licenses = api.get_licenses()
        accessories = api.get_accessories()
        consumables = api.get_consumables()
        components = api.get_components()

        # Use bulk data directly without individual API calls
        detailed_assets = []
        for asset in assets['rows']:
            supplier_info = asset.get('supplier', {})
            
            # Handle purchase_cost conversion - parse Dutch notation
            purchase_cost_raw = asset.get('purchase_cost')
            purchase_cost = 0
            
            if purchase_cost_raw and str(purchase_cost_raw).strip():
                try:
                    # Remove EUR/€, remove dots (thousand separators), replace comma with dot
                    value_str = str(purchase_cost_raw).replace('EUR', '').replace('€', '').strip()
                    value_str = value_str.replace('.', '').replace(',', '.')
                    purchase_cost = float(value_str)
                except (ValueError, TypeError):
                    purchase_cost = 0
            
            detailed_assets.append({
                'id': asset['id'],
                'name': asset.get('name', 'Unknown'),
                'asset_tag': asset.get('asset_tag', 'N/A'),
                'model': asset.get('model', {}).get('name', 'Unknown Model'),
                'supplier_id': supplier_info.get('id') if supplier_info else None,
                'supplier_name': supplier_info.get('name', 'No Supplier') if supplier_info else 'No Supplier',
                'purchase_cost': purchase_cost,
                'created_at': asset.get('created_at', {}).get('datetime', '1970-01-01T00:00:00Z'),
                'updated_at': asset.get('updated_at', {}).get('datetime', '1970-01-01T00:00:00Z')
            })
        
        # Sort by updated_at (newest first)
        detailed_assets.sort(key=lambda x: x['updated_at'], reverse=True)

        def parse_cost(raw):
            if not raw or not str(raw).strip():
                return 0
            try:
                v = str(raw).replace('EUR', '').replace('€', '').strip()
                v = v.replace('.', '').replace(',', '.')
                return float(v)
            except (ValueError, TypeError):
                return 0

        def map_items(rows, tag_key='asset_tag'):
            result = []
            for item in rows:
                supplier_info = item.get('supplier', {})
                result.append({
                    'id': item['id'],
                    'name': item.get('name', 'Unknown'),
                    'asset_tag': item.get(tag_key) or item.get('asset_tag') or f"ID:{item['id']}",
                    'model': item.get('model', {}).get('name', '') if isinstance(item.get('model'), dict) else '',
                    'supplier_id': supplier_info.get('id') if supplier_info else None,
                    'supplier_name': supplier_info.get('name', 'No Supplier') if supplier_info else 'No Supplier',
                    'purchase_cost': parse_cost(item.get('purchase_cost')),
                    'updated_at': item.get('updated_at', {}).get('datetime', '1970-01-01T00:00:00Z') if isinstance(item.get('updated_at'), dict) else '1970-01-01T00:00:00Z'
                })
            result.sort(key=lambda x: x['updated_at'], reverse=True)
            return result

        detailed_licenses = map_items(licenses.get('rows', []), tag_key='order_number')
        detailed_accessories = map_items(accessories.get('rows', []))
        detailed_consumables = map_items(consumables.get('rows', []))
        detailed_components = map_items(components.get('rows', []))

        return render_template('interactive.html',
                             assets=detailed_assets,
                             licenses=detailed_licenses,
                             accessories=detailed_accessories,
                             consumables=detailed_consumables,
                             components=detailed_components,
                             suppliers=suppliers['rows'])
    except Exception as e:
        flash(f'Error connecting to Snipe-IT: {e}', 'error')
        return render_template('interactive.html', assets=[], suppliers=[])

@app.route('/create_po', methods=['POST'])
def create_po():
    """Create purchase order with selected assets"""
    selected_assets = request.form.getlist('assets')
    supplier_id = request.form.get('supplier')
    
    if not selected_assets:
        flash('Please select at least one asset', 'error')
        return redirect(url_for('index'))
    
    if not supplier_id:
        flash('Please select a supplier', 'error')
        return redirect(url_for('index'))
    
    load_dotenv()
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'), 
                      os.getenv('VERIFY_SSL', 'true').lower() == 'true')
        
        # Get supplier info
        supplier = api.get_supplier(int(supplier_id))
        supplier_name = supplier.get('name', 'Unknown Supplier')

        # Fetch all item data in bulk for lookup
        all_items = {}
        for row in api.get_assets(limit=500).get('rows', []):
            all_items[f"asset_{row['id']}"] = row
        for row in api.get_licenses().get('rows', []):
            all_items[f"license_{row['id']}"] = row
        for row in api.get_accessories().get('rows', []):
            all_items[f"accessory_{row['id']}"] = row
        for row in api.get_consumables().get('rows', []):
            all_items[f"consumable_{row['id']}"] = row
        for row in api.get_components().get('rows', []):
            all_items[f"component_{row['id']}"] = row

        def parse_cost(raw):
            if not raw or not str(raw).strip():
                return 0
            try:
                v = str(raw).replace('EUR', '').replace('€', '').strip()
                v = v.replace('.', '').replace(',', '.')
                return float(v)
            except (ValueError, TypeError):
                return 0

        # Get selected items details
        po_items = []
        total = 0

        for entry in selected_assets:
            item = all_items.get(entry)
            if not item:
                continue
            price = parse_cost(item.get('purchase_cost'))
            category = entry.split('_')[0]
            tag = item.get('asset_tag') or item.get('order_number') or f"ID:{item['id']}"
            model = item.get('model', {}).get('name', '') if isinstance(item.get('model'), dict) else ''
            label = item.get('name', 'Unknown')
            if model:
                label = f"{label} - {model}"
            po_items.append((0, 0, tag, label, price))
            total += price

        if not po_items:
            flash('No valid items selected', 'error')
            return redirect(url_for('index'))
        
        # Get comments from form
        comments = request.form.get('comments', '').strip()
        
        # Create PO with sequential number
        po_number = get_next_po_number()
        
        po_data = {
            'po_number': po_number,
            'supplier_name': supplier_name,
            'created_at': datetime.now().strftime('%B %d, %Y'),
            'status': 'draft',
            'items': po_items,
            'total_amount': total,
            'comments': comments
        }
        
        # Generate PDF
        pdf_gen = PDFGenerator()
        output_path = f"custom_{po_number}.pdf"
        pdf_path = pdf_gen.generate_purchase_order_pdf(po_data, output_path)
        
        if os.path.exists(pdf_path):
            flash(f'Purchase Order {po_number} created successfully!', 'success')
            return send_file(pdf_path, as_attachment=True)
        else:
            flash('Error generating PDF', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error creating purchase order: {e}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
