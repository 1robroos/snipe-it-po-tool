#!/usr/bin/env python3
"""
Example script showing how to use the Snipe-IT Purchase Order Tool
"""

from src.main import PurchaseOrderTool

def main():
    try:
        # Initialize the tool
        tool = PurchaseOrderTool()
        print("✓ Successfully connected to Snipe-IT")
        
        # Example 1: Create a purchase order
        print("\n--- Creating Purchase Order ---")
        po_id = tool.create_purchase_order(
            po_number="PO-2024-001",
            supplier_id=1,  # Replace with actual supplier ID from your Snipe-IT
            asset_ids=[1, 2, 3]  # Replace with actual asset IDs from your Snipe-IT
        )
        print(f"✓ Created purchase order with ID: {po_id}")
        
        # Example 2: Generate PDF
        print("\n--- Generating PDF ---")
        pdf_path = tool.generate_po_pdf(po_id)
        print(f"✓ PDF generated: {pdf_path}")
        
        # Example 3: Show purchase order data
        print("\n--- Purchase Order Data ---")
        po_data = tool.get_po_data(po_id)
        print(f"PO Number: {po_data['po_number']}")
        print(f"Supplier: {po_data['supplier_name']}")
        print(f"Items: {len(po_data['items'])}")
        print(f"Total: ${po_data['total_amount']:.2f}")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nSetup instructions:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your Snipe-IT URL and API token")
        print("3. Install dependencies: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure:")
        print("- Your Snipe-IT instance is accessible")
        print("- Your API token has the correct permissions")
        print("- The supplier_id and asset_ids exist in your Snipe-IT")

if __name__ == "__main__":
    main()
