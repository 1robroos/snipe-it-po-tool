# 📖 Snipe-IT Purchase Order Tool - User Manual

## 🎯 Overview

The Snipe-IT Purchase Order Tool automatically generates professional PDF purchase orders from your Snipe-IT asset database. It connects directly to your Snipe-IT API to fetch real asset data and pricing.

## 🚀 Getting Started

### Accessing the Tool

#### Desktop Launcher (Easiest)
After installation, you'll find a desktop icon called **"Snipe-IT Purchase Order Tool"**:
1. Double-click the desktop icon
2. Your default browser opens automatically
3. The tool loads at `http://localhost:5001`
4. No need to remember URLs or commands

#### Web Interface (Manual)
- Open your browser and go to `http://your-server:5001`
- Bookmark this URL for easy access

#### Command Line (Advanced Users)
- Run `python3 interactive_cli.py` for text-based interface

### First Time Setup
Your system administrator will have configured:
- Connection to your Snipe-IT instance
- API authentication
- Company branding (header image)

## 📋 Creating a Purchase Order

### Step 1: Select Supplier
1. Open the web interface
2. Click the **"Select Supplier"** dropdown
3. Choose the supplier you want to create a PO for
4. The asset list will automatically filter to show only assets from that supplier

### Step 2: Choose Assets
1. Review the asset table showing:
   - **Asset Tag**: Unique identifier (sorted newest first)
   - **Asset Name**: Description of the item
   - **Model**: Product model information
   - **Supplier**: Vendor name
   - **Price**: Cost in euros (€) from Snipe-IT

2. Click on rows to select assets for your PO
3. Selected rows will be highlighted in blue
4. The total amount updates automatically

### Step 3: Add Comments (Optional)
1. Use the **"Comments/Order Instructions"** field to add:
   - Who requested the order
   - Special delivery instructions
   - Budget codes or project references
   - Any other relevant information

### Step 4: Generate Purchase Order
1. Click **"🚀 Create Purchase Order"**
2. The system will:
   - Generate a sequential PO number (e.g., ICT2025000001)
   - Create a professional PDF
   - Automatically download the file

## 📄 Understanding Your Purchase Order

### PO Number Format
- **ICT2025000001**: ICT + Year + 6-digit sequential number
- Numbers reset each year (ICT2026000001 in 2026)
- Each PO gets a unique, sequential number

### PDF Contents
Your generated PO includes:
- **Company header** (if configured)
- **PO number and date**
- **Supplier information**
- **Asset details table** with tags, names, and prices
- **Total amount** in euros
- **Comments section** (if provided)
- **Signature fields** for "Requested by" and "Management"

## 💡 Tips and Best Practices

### Asset Selection
- Assets are sorted by creation date (newest first)
- Only assets with purchase costs will appear
- Filter by supplier to see relevant items only
- Double-check asset tags match your requirements

### Comments Field Usage
Examples of useful comments:
- "Requested by: John Smith, IT Department"
- "Project: Office Renovation 2025"
- "Delivery to: Building A, 3rd Floor"
- "Budget code: IT-2025-Q1"

### Managing Purchase Orders
- Each PO is automatically numbered and dated
- Save PDFs with meaningful filenames
- Keep records of generated POs for accounting
- Coordinate with your finance team for approval process

## 🔍 Troubleshooting

### Common Issues

**"No assets found"**
- Check if the supplier has assets in Snipe-IT
- Verify assets have purchase costs entered
- Contact your Snipe-IT administrator

**"Error connecting to Snipe-IT"**
- Check your internet connection
- Contact your system administrator
- The Snipe-IT server may be temporarily unavailable

**"No valid assets selected"**
- Ensure you've clicked on asset rows to select them
- Selected rows should be highlighted in blue
- At least one asset must be selected

**PDF download doesn't start**
- Check your browser's download settings
- Disable popup blockers for this site
- Try a different browser

### Getting Help
1. **Check the total amount** - Should update when selecting assets
2. **Verify supplier selection** - Must choose a supplier first
3. **Contact your system administrator** for technical issues
4. **Check Snipe-IT data** - Ensure assets have correct information

## 📊 Features Overview

### Automatic Features
- ✅ Sequential PO numbering with yearly reset
- ✅ Real-time price calculation from Snipe-IT
- ✅ Professional PDF formatting
- ✅ Company branding integration
- ✅ Asset sorting by creation date

### User-Controlled Features
- 🎯 Supplier selection and filtering
- 📦 Individual asset selection
- 📝 Custom comments and instructions
- 💾 Instant PDF download

## 🔐 Data and Privacy

### Data Sources
- All asset information comes from your Snipe-IT database
- Prices are pulled from the purchase_cost field
- No external data sources are used

### Data Storage
- PO numbers are stored locally for sequential numbering
- No sensitive asset data is permanently stored
- Generated PDFs contain only selected information

### Security
- Direct connection to your Snipe-IT API
- No data transmitted to external services
- Secure authentication using API tokens

## 📞 Support

For technical support or questions:
1. **System Administrator**: For server/connection issues
2. **Snipe-IT Administrator**: For asset data problems
3. **Finance Team**: For PO approval processes
4. **IT Help Desk**: For general technical assistance

---

**Version**: Latest
**Last Updated**: November 2025
**Compatible with**: Snipe-IT v6.0+
