import weasyprint
from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict, List

def format_dutch_currency(amount):
    """Format amount to Dutch currency notation: €1.234,56"""
    if amount == 0:
        return "€0,00"
    
    # Format with 2 decimals
    formatted = f"{amount:.2f}"
    
    # Split into euros and cents
    euros, cents = formatted.split('.')
    
    # Add thousand separators (dots) to euros part
    if len(euros) > 3:
        # Reverse, add dots every 3 digits, reverse back
        euros_reversed = euros[::-1]
        euros_with_dots = '.'.join([euros_reversed[i:i+3] for i in range(0, len(euros_reversed), 3)])
        euros = euros_with_dots[::-1]
    
    return f"€{euros},{cents}"

class PDFGenerator:
    def __init__(self, template_dir: str = 'templates', static_dir: str = 'static'):
        self.template_dir = template_dir
        self.static_dir = static_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        # Add custom filter
        self.env.filters['dutch_currency'] = format_dutch_currency
    
    def generate_purchase_order_pdf(self, po_data: Dict, output_path: str) -> str:
        """Generate PDF from purchase order data"""
        
        # Load template
        template = self.env.get_template('purchase_order.html')
        
        # Render HTML
        html_content = template.render(**po_data)
        
        # Load CSS if exists
        css_path = os.path.join(self.static_dir, 'purchase_order.css')
        stylesheets = []
        if os.path.exists(css_path):
            stylesheets.append(weasyprint.CSS(filename=css_path))
        
        # Generate PDF with base_url for images - use explicit weasyprint.HTML
        base_url = f"file://{os.path.abspath('.')}/"
        html_doc = weasyprint.HTML(string=html_content, base_url=base_url)
        html_doc.write_pdf(output_path, stylesheets=stylesheets)
        
        return output_path
