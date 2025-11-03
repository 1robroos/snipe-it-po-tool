# 🛒 Snipe-IT Purchase Order Tool

Automatically generate professional PDF purchase orders from your Snipe-IT assets, with company branding and real purchase costs.

## ✨ Features

- 🔗 **Direct Snipe-IT Integration** - Connects to your Snipe-IT API
- 🎯 **Custom Asset Selection** - Choose exactly which assets to include
- 💰 **Real Purchase Costs** - Uses actual purchase costs from Snipe-IT
- 🏢 **Supplier-Specific POs** - Automatic supplier filtering and grouping
- 🎨 **Company Branding** - Professional PDFs with company header
- 📄 **Professional Layout** - Clean, printable purchase order documents
- 🔢 **Sequential PO Numbers** - ICT0000001, ICT0000002, etc.
- 🌐 **Web Interface** - Easy-to-use browser interface
- ⚡ **Command Line** - Interactive CLI option

## 🚀 Quick Start

### Option 1: Desktop Icon (Easiest)
```bash
./install.sh
# Double-click the desktop icon "Snipe-IT Purchase Order Tool"
# Browser opens automatically to http://localhost:5001
```

### Option 2: One-Click Startup Script
```bash
./install.sh
./start_web_app.sh
# Browser opens automatically
```

### Option 3: Manual Web Interface
```bash
./install.sh
python3 interactive_web_app.py
# Open browser to: http://localhost:5001
```

### Option 4: Interactive Command Line
```bash
./install.sh
python3 interactive_cli.py
```

## 🖥️ VM Deployment

For production deployment on virtual machines:

```bash
# Create deployment package
./create_package.sh

# Copy to VM
scp /tmp/snipe-po-tool-YYYYMMDD.tar.gz user@vm-ip:~/

# Deploy on VM
tar -xzf snipe-po-tool-YYYYMMDD.tar.gz
cd snipe-po-tool-YYYYMMDD
./deploy.sh
```

See `DEPLOYMENT.md` for detailed VM deployment instructions.

## ⚙️ Configuration

1. **Get Snipe-IT API Token:**
   - Login to your Snipe-IT instance
   - Go to Account Settings > API Keys
   - Generate new token

2. **Edit .env file:**
```bash
SNIPE_URL=http://your-snipe-it-url
SNIPE_TOKEN=your-api-token-here
VERIFY_SSL=false  # Set to true for production with valid SSL
```

3. **Add Company Header (Optional):**
   - Place your company header image in `static/` folder
   - Supported formats: JPG, PNG
   - Recommended size: Max height 120px

## 📋 Usage

**Interactive Web Interface:**
- Visit http://localhost:5001
- Select supplier from dropdown
- Choose assets by clicking on cards
- Quantities are adjustable, prices come from Snipe-IT
- Click "Create Purchase Order"
- Download PDF immediately

**Interactive Command Line:**
```bash
python3 interactive_cli.py
# Follow prompts to:
# 1. Select supplier
# 2. Choose assets (1,2,3 or 'all')
# 3. Set quantities (prices from Snipe-IT)
# 4. Generate PDF
```

## 📁 Output

The tool generates:
- Sequential PO numbers: `ICT0000001`, `ICT0000002`, etc.
- Professional PDF layout with company header
- Itemized asset lists with real purchase costs from Snipe-IT
- Automatic handling of comma-formatted prices (e.g., "1,701.00")
- Supplier-specific grouping
- Total amounts per purchase order
- Signature fields for approval

## 🎯 Key Features

- **Real Pricing**: Uses purchase_cost field from Snipe-IT assets
- **Asset Selection**: Choose specific assets per PO
- **Supplier Filtering**: Only see assets from selected supplier
- **Company Branding**: Automatic header image inclusion
- **Sequential Numbering**: ICT0000001, ICT0000002, etc.
- **Error Handling**: Graceful handling of missing suppliers/costs
- **Real-time Totals**: See total amount as you build PO
- **Instant PDF**: Download immediately after creation

## 🔧 Requirements

- Python 3.7+
- Snipe-IT with API access
- Internet connection to Snipe-IT instance
- Dependencies: flask, python-dotenv, requests, reportlab

## 📞 Support

For issues or questions, contact your system administrator.

## 🚀 Production Deployment

The tool includes complete VM deployment automation:
- Systemd service configuration
- Automatic startup on boot
- SSL verification handling
- Professional PDF generation with reportlab
- Sequential PO numbering system
