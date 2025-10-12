#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from snipe_api import SnipeAPI
from pdf_generator import PDFGenerator

# Load environment variables
load_dotenv()

class PurchaseOrderTool:
    def __init__(self):
        self.snipe_url = os.getenv('SNIPE_URL')
        self.snipe_token = os.getenv('SNIPE_TOKEN')
        
        if not self.snipe_url or not self.snipe_token:
            raise ValueError("Please set SNIPE_URL and SNIPE_TOKEN in .env file")
        
        self.api = SnipeAPI(self.snipe_url, self.snipe_token)
        self.pdf_gen = PDFGenerator()
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for purchase orders"""
        db_path = os.path.join('data', 'purchase_orders.db')
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
    
    def create_purchase_order(self, po_number: str, supplier_id: int, asset_ids: list):
        """Create a new purchase order"""
        # Get supplier info
        supplier_data = self.api.get_supplier(supplier_id)
        supplier_name = supplier_data.get('name', 'Unknown Supplier')
        
        # Create PO in database
        db_path = os.path.join('data', 'purchase_orders.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO purchase_orders (po_number, supplier_id, supplier_name)
            VALUES (?, ?, ?)
        ''', (po_number, supplier_id, supplier_name))
        
        po_id = cursor.lastrowid
        
        # Add items
        for asset_id in asset_ids:
            asset_data = self.api.get_asset(asset_id)
            asset_name = asset_data.get('name', f'Asset {asset_id}')
            purchase_cost = asset_data.get('purchase_cost', {}).get('value', 0) if isinstance(asset_data.get('purchase_cost'), dict) else 0
            
            cursor.execute('''
                INSERT INTO purchase_order_items (po_id, asset_id, asset_name, unit_price)
                VALUES (?, ?, ?, ?)
            ''', (po_id, asset_id, asset_name, purchase_cost))
        
        conn.commit()
        conn.close()
        
        return po_id
    
    def generate_po_pdf(self, po_id: int, output_dir: str = 'output'):
        """Generate PDF for purchase order"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Get PO data from database
        po_data = self.get_po_data(po_id)
        
        # Generate PDF
        filename = f"PO_{po_data['po_number']}.pdf"
        output_path = os.path.join(output_dir, filename)
        
        return self.pdf_gen.generate_purchase_order_pdf(po_data, output_path)
    
    def get_po_data(self, po_id: int):
        """Get purchase order data for PDF generation"""
        db_path = os.path.join('data', 'purchase_orders.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get PO info
        cursor.execute('SELECT * FROM purchase_orders WHERE id = ?', (po_id,))
        po = cursor.fetchone()
        
        if not po:
            conn.close()
            raise ValueError(f"Purchase order with ID {po_id} not found")
        
        # Get items
        cursor.execute('SELECT * FROM purchase_order_items WHERE po_id = ?', (po_id,))
        items = cursor.fetchall()
        
        conn.close()
        
        # Calculate total
        total_amount = sum(item[3] * item[4] for item in items)  # quantity * unit_price
        
        return {
            'po_number': po[1],
            'supplier_name': po[3],
            'created_at': datetime.now().strftime('%B %d, %Y'),
            'status': po[5],
            'items': items,
            'total_amount': total_amount
        }

def main():
    """Example usage"""
    print("Snipe-IT Purchase Order Tool")
    print("=" * 40)
    
    try:
        tool = PurchaseOrderTool()
        print("✓ Connected to Snipe-IT API")
        print("✓ Database initialized")
        
        # Example: Create a purchase order
        print("\nExample usage:")
        print("po_id = tool.create_purchase_order('PO-2024-001', supplier_id=1, asset_ids=[1, 2, 3])")
        print("pdf_path = tool.generate_po_pdf(po_id)")
        print("print(f'PDF generated: {pdf_path}')")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Set your SNIPE_URL and SNIPE_TOKEN in .env")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
