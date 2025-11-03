import weasyprint
from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict, List

class PDFGenerator:
    def __init__(self, template_dir: str = 'templates', static_dir: str = 'static'):
        self.template_dir = template_dir
        self.static_dir = static_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
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
