#!/bin/bash

# Create deployment package for VM installation

PACKAGE_NAME="snipe-po-tool-$(date +%Y%m%d)"
TEMP_DIR="/tmp/$PACKAGE_NAME"

echo "📦 Creating deployment package: $PACKAGE_NAME"

# Create temporary directory
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

# Copy essential files
cp -r src/ templates/ static/ data/ $TEMP_DIR/
cp *.py requirements.txt .env.example README.md deploy.sh $TEMP_DIR/

# Create package archive
cd /tmp
tar -czf "$PACKAGE_NAME.tar.gz" $PACKAGE_NAME/

echo "✅ Package created: /tmp/$PACKAGE_NAME.tar.gz"
echo ""
echo "📋 To deploy on VM:"
echo "1. Copy package to VM: scp /tmp/$PACKAGE_NAME.tar.gz user@vm-ip:~/"
echo "2. Extract: tar -xzf $PACKAGE_NAME.tar.gz"
echo "3. Deploy: cd $PACKAGE_NAME && ./deploy.sh"

# Cleanup
rm -rf $TEMP_DIR
