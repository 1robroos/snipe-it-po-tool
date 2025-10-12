#!/usr/bin/env python3
"""
Debug PDF generation issue
"""

from weasyprint import HTML
import traceback

def test_minimal_pdf():
    """Test minimal PDF generation"""
    try:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body><h1>Test PDF</h1></body>
        </html>
        """
        
        print("Creating HTML object...")
        html_doc = HTML(string=html_content)
        
        print("Writing PDF...")
        html_doc.write_pdf('test_minimal.pdf')
        
        print("✓ Minimal PDF test successful")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_minimal_pdf()
