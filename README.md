# 🛒 Snipe-IT Purchase Order Tool

Automatically generate professional PDF purchase orders from your Snipe-IT assets, with company branding and real purchase costs.

## ✨ Features

- 🔗 **Direct Snipe-IT Integration** - Connects to your Snipe-IT API
- 🎯 **Item Selection** - Choose assets, licenses, accessories, consumables or components
- 💰 **Real Purchase Costs** - Uses actual purchase costs from Snipe-IT
- 🏢 **Supplier-Specific POs** - Automatic supplier filtering and grouping
- 🎨 **Company Branding** - Professional PDFs with company header
- 📄 **Professional Layout** - Clean, printable purchase order documents
- 🔢 **Sequential PO Numbers** - ICT2025000001, ICT2025000002, etc. (yearly reset)
- 🌐 **Web Interface** - Easy-to-use browser interface
- ⚡ **Command Line** - Interactive CLI option
- 📝 **Comments Field** - Add order instructions and requester info
- 🏷️ **Asset Tags** - Display asset tags / order numbers in first column, sorted newest first
- 💶 **Euro Currency** - All prices displayed in euros

## 🚀 Quick Start (Development/Local)

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

### Test Environment Deployment
For test/development environments (self-signed certificates):

```bash
# Create deployment package
./create_package.sh

# Copy to test VM
scp /tmp/snipe-po-tool-YYYYMMDD.tar.gz user@test-vm-ip:~/

# Deploy on test VM
tar -xzf snipe-po-tool-YYYYMMDD.tar.gz
cd snipe-po-tool-YYYYMMDD
./deploy.sh

# Configure for test environment
sudo nano /opt/snipe-po-tool/.env
```

Test environment .env configuration:
```bash
SNIPE_URL=https://your-test-snipe-it-url
SNIPE_TOKEN=your-api-token-here
VERIFY_SSL=false  # Disabled for test environments
```

### Production Environment Deployment
For production environments (valid SSL certificates):

```bash
# Create deployment package
./create_package.sh

# Copy to production VM
scp /tmp/snipe-po-tool-YYYYMMDD.tar.gz user@prod-vm-ip:~/

# Deploy on production VM
tar -xzf snipe-po-tool-YYYYMMDD.tar.gz
cd snipe-po-tool-YYYYMMDD
./deploy.sh

# Configure for production environment
sudo nano /opt/snipe-po-tool/.env
```

Production environment .env configuration:
```bash
SNIPE_URL=https://your-production-snipe-it-url
SNIPE_TOKEN=your-api-token-here
VERIFY_SSL=true  # Enabled for production with valid certificates
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
- Visit http://localhost:5001 (local) or http://vm-ip:5001 (VM)
- Select supplier from dropdown
- Choose items from tabbed table: Assets, Licenses, Accessories, Consumables, Components
- Add comments/order instructions
- Click "Create Purchase Order"
- Download PDF immediately

**Interactive Command Line:**
```bash
python3 interactive_cli.py
# Follow prompts to:
# 1. Select supplier
# 2. Choose assets
# 3. Add comments
# 4. Generate PDF
```

## 📁 Output

The tool generates:
- Sequential PO numbers: `ICT2025000001`, `ICT2025000002`, etc.
- Yearly reset: `ICT2026000001` starts in 2026
- Professional PDF layout with company header
- Asset table with tags, names, models, and euro prices
- Comments/order instructions section
- Signature fields for "Requested by" and "Management"
- Clean layout without redundant information

## 🎯 Key Features

- **Real Pricing**: Uses purchase_cost field from Snipe-IT assets
- **Item Selection**: Choose assets, licenses, accessories, consumables or components per PO
- **Supplier Filtering**: Only see items from selected supplier
- **Company Branding**: Automatic header image inclusion
- **Sequential Numbering**: ICT2025000001, ICT2025000002, etc. (yearly reset)
- **Asset Tags**: First column shows asset tags or order numbers (licenses)
- **Sorting**: Assets sorted by creation date (newest first)
- **Comments**: Free text field for order instructions
- **Euro Currency**: All prices in euros (€)
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

## 🚀 Production vs Test Deployment

**Test Environment:**
- Self-signed or invalid SSL certificates
- `VERIFY_SSL=false` in .env
- Typically used for development/testing

**Production Environment:**
- Valid SSL certificates
- `VERIFY_SSL=true` in .env
- Used for live business operations

The tool automatically handles SSL verification based on the VERIFY_SSL setting in your .env configuration.
