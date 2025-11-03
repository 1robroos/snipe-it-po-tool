from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import os
from typing import Dict

class PDFGenerator:
    def __init__(self, template_dir: str = 'templates', static_dir: str = 'static'):
        self.template_dir = template_dir
        self.static_dir = static_dir
    
    def generate_purchase_order_pdf(self, po_data: Dict, output_path: str) -> str:
        """Generate PDF using reportlab with improved layout"""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter, 
                              topMargin=0.5*inch, bottomMargin=0.5*inch,
                              leftMargin=0.5*inch, rightMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Company Header Image
        header_path = os.path.join(self.static_dir, 'GTE Group Header.jpg')
        if os.path.exists(header_path):
            try:
                img = Image(header_path, width=7*inch, height=1.2*inch)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 20))
            except:
                pass
        
        # Header with PO title and number
        header_table = Table([
            ['PURCHASE ORDER', po_data.get('po_number', 'N/A')],
            ['', f"Date: {po_data.get('created_at', po_data.get('date', 'N/A'))}"]
        ], colWidths=[4*inch, 3*inch])
        
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (0,0), 24),
            ('FONTNAME', (1,0), (1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (1,0), (1,0), 20),
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (1,0), (1,1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(header_table)
        
        # Separator line
        line_table = Table([['_' * 100]], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ]))
        story.append(line_table)
        
        # PO Details and Supplier Info
        details_data = [
            ['PO Number:', po_data.get('po_number', 'N/A'), 'Status:', po_data.get('status', 'draft').upper()],
            ['Created:', po_data.get('created_at', po_data.get('date', 'N/A')), 'Supplier:', po_data.get('supplier_name', 'N/A')]
        ]
        
        details_table = Table(details_data, colWidths=[1.2*inch, 2.3*inch, 1.2*inch, 2.3*inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        # Items section title
        items_title = Paragraph(f"<b>Items ({len(po_data.get('items', []))})</b>", 
                               ParagraphStyle('ItemsTitle', parent=styles['Normal'], 
                                            fontSize=14, spaceAfter=10))
        story.append(items_title)
        
        # Items table
        items_data = [['#', 'Asset Name', 'Qty', 'Unit Price', 'Total Price', 'Notes']]
        
        total_amount = 0
        for idx, item in enumerate(po_data.get('items', []), 1):
            # Handle both tuple and dict formats
            if isinstance(item, tuple):
                asset_id = item[2] if len(item) > 2 else 'N/A'
                name = item[3] if len(item) > 3 else 'Unknown'
                price = float(str(item[4]).replace(',', '').replace('$', '') or 0) if len(item) > 4 else 0
                qty = item[5] if len(item) > 5 else 1
            else:
                asset_id = item.get('asset_tag', item.get('id', 'N/A'))
                name = item.get('name', 'Unknown')
                price = float(str(item.get('purchase_cost', '0')).replace(',', '').replace('$', '') or 0)
                qty = item.get('quantity', 1)
            
            total = qty * price
            total_amount += total
            
            items_data.append([
                str(idx),
                str(name),
                str(qty),
                f"${price:.2f}",
                f"${total:.2f}",
                '-'
            ])
        
        # Add total row
        items_data.append(['', '', '', 'TOTAL:', f"${total_amount:.2f}", ''])
        
        items_table = Table(items_data, colWidths=[0.4*inch, 2.5*inch, 0.6*inch, 1*inch, 1*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            
            # Data rows
            ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-2), 11),
            ('ALIGN', (0,1), (0,-1), 'CENTER'),  # # column
            ('ALIGN', (2,1), (2,-1), 'CENTER'),  # Qty column
            ('ALIGN', (3,1), (-2,-1), 'RIGHT'),  # Price columns
            
            # Total row
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightblue),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,-1), (-1,-1), 12),
            ('ALIGN', (3,-1), (4,-1), 'RIGHT'),
            
            # Grid
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(items_table)
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = f"This purchase order was generated on {po_data.get('created_at', po_data.get('date', 'N/A'))}."
        footer = Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], 
                                                      fontSize=10, textColor=colors.grey))
        story.append(footer)
        
        # Signature section
        story.append(Spacer(1, 40))
        sig_data = [
            ['Client', 'Management'],
            ['', ''],
            ['', ''],
            ['Signature & Date', 'Signature & Date']
        ]
        
        sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch], rowHeights=[20, 40, 20, 20])
        sig_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,3), (-1,3), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LINEBELOW', (0,1), (-1,1), 2, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(sig_table)
        
        doc.build(story)
        return output_path
