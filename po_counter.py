import os
import json
from datetime import datetime

def get_next_po_number():
    """Generate next sequential PO number with yearly reset"""
    counter_file = "data/po_counter.json"
    current_year = datetime.now().year
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Read current counter
    if os.path.exists(counter_file):
        try:
            with open(counter_file, 'r') as f:
                data = json.load(f)
                stored_year = data.get('year', current_year)
                counter = data.get('counter', 0)
                
                # Reset counter if new year
                if stored_year != current_year:
                    counter = 0
        except:
            counter = 0
    else:
        counter = 0
    
    # Increment counter
    counter += 1
    
    # Save new counter with current year
    with open(counter_file, 'w') as f:
        json.dump({'year': current_year, 'counter': counter}, f)
    
    # Format PO number: ICT + year + 6-digit counter
    po_number = f"ICT{current_year}{counter:06d}"
    return po_number
