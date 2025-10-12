#!/usr/bin/env python3
"""
Simple test to verify the tool works without real API calls
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.append('src')

from pdf_generator import PDFGenerator

def test_pdf_generation():
    """Test PDF generation with sample data"""
    print("Testing PDF generation...")
    
    # Sample purchase order data
    sample_data = {
        'po_number': 'PO-TEST-001',
        'supplier_name': 'Test Supplier Inc.',
        'created_at': datetime.now().strftime('%B %d, %Y'),
        'status': 'draft',
        'items': [
            (1, 1, 'Dell Laptop Model XYZ', 1, 899.99),  # id, po_id, asset_name, quantity, unit_price
            (2, 1, 'HP Monitor 24"', 2, 199.99),
            (3, 1, 'Wireless Mouse', 3, 29.99)
        ],
        'total_amount': 1389.96
    }
    
    # Generate PDF
    pdf_gen = PDFGenerator()
    output_path = 'test_purchase_order.pdf'
    
    try:
        result = pdf_gen.generate_purchase_order_pdf(sample_data, output_path)
        print(f"✓ PDF generated successfully: {result}")
        
        # Check if file exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ File size: {file_size} bytes")
            return True
        else:
            print("❌ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    
    try:
        import sqlite3
        
        # Test database creation
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect('data/test.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        conn.commit()
        
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            print("✓ Database operations work correctly")
            return True
        else:
            print("❌ Database test failed")
            return False
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("Snipe-IT Purchase Order Tool - Test Suite")
    print("=" * 50)
    
    # Test PDF generation
    pdf_success = test_pdf_generation()
    
    # Test database
    db_success = test_database()
    
    print("\n" + "=" * 50)
    if pdf_success and db_success:
        print("✅ All tests passed! The tool is ready to use.")
        print("\nNext steps:")
        print("1. Update .env with your real Snipe-IT URL and API token")
        print("2. Run: python example.py")
    else:
        print("❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
