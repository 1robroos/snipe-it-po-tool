#!/usr/bin/env python3

import sys
import traceback

try:
    from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
    print("✓ Flask imported")
    
    import os
    from datetime import datetime
    from dotenv import load_dotenv
    print("✓ Basic imports OK")

    sys.path.append('src')
    from snipe_api import SnipeAPI
    print("✓ SnipeAPI imported")
    
    from pdf_generator import PDFGenerator
    print("✓ PDFGenerator imported")
    
    # Test PDFGenerator creation
    pdf_gen = PDFGenerator()
    print("✓ PDFGenerator created successfully")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()

print("Debug complete")
