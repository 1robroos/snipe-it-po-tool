# Snipe-IT Purchase Order Tool

A standalone Python tool to create purchase orders from Snipe-IT assets via API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Edit `.env` with your Snipe-IT details:
- `SNIPE_URL`: Your Snipe-IT instance URL
- `SNIPE_TOKEN`: Your API token from Snipe-IT

## Usage

```python
from src.main import PurchaseOrderTool

tool = PurchaseOrderTool()

# Create purchase order
po_id = tool.create_purchase_order(
    po_number="PO-2024-001",
    supplier_id=1,
    asset_ids=[1, 2, 3]
)

# Generate PDF
pdf_path = tool.generate_po_pdf(po_id)
print(f"PDF generated: {pdf_path}")
```

## Project Structure

- `src/` - Python source code
- `templates/` - HTML templates for PDF generation
- `static/` - CSS files for styling
- `data/` - SQLite database storage
- `output/` - Generated PDF files

## Next Steps

1. Add your HTML template from the Snipe-IT PR to `templates/purchase_order.html`
2. Add corresponding CSS to `static/purchase_order.css`
3. Test with your Snipe-IT instance
