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
    """Extract purchase cost from asset detail"""
    purchase_cost = asset_detail.get('purchase_cost', {})
    if isinstance(purchase_cost, dict):
        amount = purchase_cost.get('amount', 0)
        if isinstance(amount, str):
            # Remove commas from price strings like "1,701.00"
            amount = amount.replace(',', '')
        return float(amount) if amount else 0
    else:
        if isinstance(purchase_cost, str):
            # Remove commas from price strings
            purchase_cost = purchase_cost.replace(',', '')
        return float(purchase_cost) if purchase_cost else 0

@app.route('/')
def index():
    """Main page with asset selection"""
    load_dotenv()
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'), 
                      os.getenv('VERIFY_SSL', 'true').lower() == 'true')
        assets = api.get_assets(limit=500)
        suppliers = api.get_suppliers()
        
        # Use bulk data directly without individual API calls
        detailed_assets = []
        for asset in assets['rows']:
            supplier_info = asset.get('supplier', {})
            
            # Handle purchase_cost conversion
            purchase_cost = asset.get('purchase_cost', 0)
            if isinstance(purchase_cost, str):
                try:
                    purchase_cost = float(purchase_cost.replace(',', '.'))
                except (ValueError, AttributeError):
                    purchase_cost = 0
            elif purchase_cost is None:
                purchase_cost = 0
            
            detailed_assets.append({
                'id': asset['id'],
                'name': asset.get('name', 'Unknown'),
                'asset_tag': asset.get('asset_tag', 'N/A'),
                'model': asset.get('model', {}).get('name', 'Unknown Model'),
                'supplier_id': supplier_info.get('id') if supplier_info else None,
                'supplier_name': supplier_info.get('name', 'No Supplier') if supplier_info else 'No Supplier',
                'purchase_cost': purchase_cost,
                'created_at': asset.get('created_at', {}).get('datetime', '1970-01-01T00:00:00Z')
            })
        
        # Sort by creation date (newest first)
        detailed_assets.sort(key=lambda x: x['created_at'], reverse=True)
        
        return render_template('interactive.html', 
                             assets=detailed_assets,
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
        
        # Get selected assets details
        po_items = []
        total = 0
        
        for asset_id in selected_assets:
            try:
                asset = api.get_asset(int(asset_id))
                # Use purchase_cost from Snipe-IT, fallback to 0 if not set
                purchase_cost = asset.get('purchase_cost', {})
                if isinstance(purchase_cost, dict):
                    amount = purchase_cost.get('amount', 0)
                    if isinstance(amount, str):
                        amount = amount.replace(',', '')
                    price = float(amount) if amount else 0
                else:
                    if isinstance(purchase_cost, str):
                        purchase_cost = purchase_cost.replace(',', '')
                    price = float(purchase_cost) if purchase_cost else 0
                
                po_items.append((
                    0, 0, 
                    asset.get('asset_tag', 'N/A'),  # Asset tag
                    f"{asset.get('name', 'Unknown')} - {asset.get('model', {}).get('name', 'Unknown Model')}",
                    price  # Price in euros
                ))
                total += price
            except Exception as e:
                flash(f'Error processing asset {asset_id}: {e}', 'error')
                continue
        
        if not po_items:
            flash('No valid assets selected', 'error')
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
