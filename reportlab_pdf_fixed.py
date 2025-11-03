from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from typing import Dict

class PDFGenerator:
    def __init__(self, template_dir: str = 'templates', static_dir: str = 'static'):
        self.template_dir = template_dir
        self.static_dir = static_dir
    
    def generate_purchase_order_pdf(self, po_data: Dict, output_path: str) -> str:
        """Generate PDF using reportlab"""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], 
                                   fontSize=24, spaceAfter=30)
        story.append(Paragraph("PURCHASE ORDER", title_style))
        
        # PO Info
        po_info = [
            ['PO Number:', po_data.get('po_number', 'N/A')],
            ['Date:', po_data.get('date', 'N/A')],
            ['Supplier:', po_data.get('supplier_name', 'N/A')]
        ]
        
        info_table = Table(po_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Items table
        items_data = [['Asset ID', 'Name', 'Qty', 'Unit Price', 'Total']]
        
        total_amount = 0
        for item in po_data.get('items', []):
            # Handle both tuple and dict formats
            if isinstance(item, tuple):
                # Tuple format: (0, 0, asset_id, name, purchase_cost, quantity)
                asset_id = item[2] if len(item) > 2 else 'N/A'
                name = item[3] if len(item) > 3 else 'Unknown'
                price = float(str(item[4]).replace(',', '').replace('$', '') or 0) if len(item) > 4 else 0
                qty = item[5] if len(item) > 5 else 1
            else:
                # Dict format
                asset_id = item.get('asset_tag', item.get('id', 'N/A'))
                name = item.get('name', 'Unknown')
                price = float(str(item.get('purchase_cost', '0')).replace(',', '').replace('$', '') or 0)
                qty = item.get('quantity', 1)
            
            total = qty * price
            total_amount += total
            
            items_data.append([
                str(asset_id),
                str(name),
                str(qty),
                f"${price:.2f}",
                f"${total:.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[1*inch, 3*inch, 0.5*inch, 1*inch, 1*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(items_table)
        
        # Total
        story.append(Spacer(1, 20))
        total_para = Paragraph(f"<b>TOTAL: ${total_amount:.2f}</b>", 
                              ParagraphStyle('Total', parent=styles['Normal'], 
                                           fontSize=16, alignment=2))
        story.append(total_para)
        
        doc.build(story)
        return output_path
