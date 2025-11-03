import os
import json

def get_next_po_number(prefix="ICT", digits=7):
    """Generate next sequential PO number"""
    counter_file = "data/po_counter.json"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Read current counter
    if os.path.exists(counter_file):
        try:
            with open(counter_file, 'r') as f:
                data = json.load(f)
                counter = data.get('counter', 0)
        except:
            counter = 0
    else:
        counter = 0
    
    # Increment counter
    counter += 1
    
    # Save new counter
    with open(counter_file, 'w') as f:
        json.dump({'counter': counter}, f)
    
    # Format PO number
    po_number = f"{prefix}{counter:0{digits}d}"
    return po_number
