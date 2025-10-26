#!/usr/bin/env python3
"""
Simple web interface for Purchase Order generation
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append('src')
from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    """Main page"""
    load_dotenv()
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
        assets = api.get_assets()
        suppliers = api.get_suppliers()
        
        return render_template('index.html', 
                             assets_count=assets['total'],
                             suppliers_count=suppliers['total'])
    except Exception as e:
        flash(f'Error connecting to Snipe-IT: {e}', 'error')
        return render_template('index.html', assets_count=0, suppliers_count=0)

@app.route('/generate', methods=['POST'])
def generate_po():
    """Generate purchase orders"""
    load_dotenv()
    
    try:
        api = SnipeAPI(os.getenv('SNIPE_URL'), os.getenv('SNIPE_TOKEN'))
        
        # Get assets grouped by supplier
        assets = api.get_assets()
        supplier_assets = {}
        
        for asset in assets['rows']:
            try:
                asset_detail = api.get_asset(asset['id'])
                supplier_name = asset_detail.get('supplier', {}).get('name', 'No Supplier') if asset_detail.get('supplier') else 'No Supplier'
                
                if supplier_name not in supplier_assets:
                    supplier_assets[supplier_name] = []
                
                supplier_assets[supplier_name].append({
                    'name': asset.get('name', 'Unknown'),
                    'model': asset.get('model', {}).get('name', 'Unknown Model'),
                    'id': asset['id']
                })
            except:
                continue
        
        # Generate POs
        generated_files = []
        
        for supplier_name, assets_list in supplier_assets.items():
            if not assets_list:
                continue
                
            po_number = f"PO-{supplier_name.upper().replace(' ', '')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            formatted_items = []
            total = 0
            
            for asset in assets_list:
                price = 299.99 if 'pc' in asset['name'].lower() else 149.99
                formatted_items.append((0, 0, asset['id'], f"{asset['name']} - {asset['model']}", 1, price))
                total += price
            
            po_data = {
                'po_number': po_number,
                'supplier_name': supplier_name,
                'created_at': datetime.now().strftime('%B %d, %Y'),
                'status': 'draft',
                'items': formatted_items,
                'total_amount': total
            }
            
            pdf_gen = PDFGenerator()
            output_path = f"web_{po_number}.pdf"
            pdf_path = pdf_gen.generate_purchase_order_pdf(po_data, output_path)
            
            if os.path.exists(pdf_path):
                generated_files.append((supplier_name, pdf_path, total))
        
        flash(f'Generated {len(generated_files)} purchase orders!', 'success')
        return render_template('results.html', files=generated_files)
        
    except Exception as e:
        flash(f'Error generating POs: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated PDF"""
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
