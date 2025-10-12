#!/usr/bin/env python3
"""
Demo script showing the Snipe-IT Purchase Order Tool with sample data
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add src to path
sys.path.append('src')

from pdf_generator import PDFGenerator

def create_demo_purchase_order():
    """Create a demo purchase order with sample data"""
    print("Creating demo purchase order...")
    
    # Initialize database
    os.makedirs('data', exist_ok=True)
    db_path = os.path.join('data', 'demo_purchase_orders.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_number TEXT UNIQUE NOT NULL,
            supplier_id INTEGER,
            supplier_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_id INTEGER,
            asset_id INTEGER,
            asset_name TEXT,
            quantity INTEGER DEFAULT 1,
            unit_price DECIMAL(10,2),
            FOREIGN KEY (po_id) REFERENCES purchase_orders (id)
        )
    ''')
    
    # Insert demo purchase order
    cursor.execute('''
        INSERT OR REPLACE INTO purchase_orders (po_number, supplier_id, supplier_name, status)
        VALUES (?, ?, ?, ?)
    ''', ('PO-DEMO-2024-001', 1, 'TechSupply Solutions Inc.', 'draft'))
    
    po_id = cursor.lastrowid
    
    # Insert demo items
    demo_items = [
        (1, 'Dell OptiPlex 7090 Desktop', 5, 899.99),
        (2, 'HP EliteDisplay 24" Monitor', 5, 249.99),
        (3, 'Logitech MX Master 3 Mouse', 5, 99.99),
        (4, 'Dell Wireless Keyboard KB216', 5, 29.99),
        (5, 'Webcam HD Pro C920', 3, 79.99)
    ]
    
    for asset_id, asset_name, quantity, unit_price in demo_items:
        cursor.execute('''
            INSERT OR REPLACE INTO purchase_order_items (po_id, asset_id, asset_name, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (po_id, asset_id, asset_name, quantity, unit_price))
    
    conn.commit()
    conn.close()
    
    return po_id

def get_demo_po_data(po_id):
    """Get demo purchase order data"""
    db_path = os.path.join('data', 'demo_purchase_orders.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get PO info
    cursor.execute('SELECT * FROM purchase_orders WHERE id = ?', (po_id,))
    po = cursor.fetchone()
    
    # Get items
    cursor.execute('SELECT * FROM purchase_order_items WHERE po_id = ?', (po_id,))
    items = cursor.fetchall()
    
    conn.close()
    
    # Calculate total - items structure: (id, po_id, asset_id, asset_name, quantity, unit_price)
    total_amount = sum(float(item[4]) * float(item[5]) for item in items)  # quantity * unit_price
    
    return {
        'po_number': po[1],
        'supplier_name': po[3],
        'created_at': datetime.now().strftime('%B %d, %Y'),
        'status': po[5],
        'items': items,
        'total_amount': total_amount
    }

def main():
    print("🛒 Snipe-IT Purchase Order Tool - Demo")
    print("=" * 50)
    
    try:
        # Create demo purchase order
        po_id = create_demo_purchase_order()
        print(f"✓ Created demo purchase order with ID: {po_id}")
        
        # Get purchase order data
        po_data = get_demo_po_data(po_id)
        print(f"✓ PO Number: {po_data['po_number']}")
        print(f"✓ Supplier: {po_data['supplier_name']}")
        print(f"✓ Items: {len(po_data['items'])}")
        print(f"✓ Total: ${po_data['total_amount']:.2f}")
        
        # Generate PDF
        print("\n📄 Generating PDF...")
        pdf_gen = PDFGenerator()
        output_path = f"demo_{po_data['po_number']}.pdf"
        
        pdf_path = pdf_gen.generate_purchase_order_pdf(po_data, output_path)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF generated successfully!")
            print(f"   📁 File: {pdf_path}")
            print(f"   📊 Size: {file_size:,} bytes")
            
            # Show item details
            print(f"\n📋 Purchase Order Details:")
            print(f"   PO Number: {po_data['po_number']}")
            print(f"   Supplier: {po_data['supplier_name']}")
            print(f"   Date: {po_data['created_at']}")
            print(f"   Status: {po_data['status'].upper()}")
            print(f"\n   Items:")
            for item in po_data['items']:
                asset_name = item[3]  # asset_name is at index 3
                quantity = item[4]    # quantity is at index 4
                unit_price = item[5]  # unit_price is at index 5
                total_price = float(quantity) * float(unit_price)
                print(f"   • {asset_name}")
                print(f"     Qty: {quantity} × ${float(unit_price):.2f} = ${total_price:.2f}")
            
            print(f"\n   💰 TOTAL: ${po_data['total_amount']:.2f}")
            
        else:
            print("❌ PDF generation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
