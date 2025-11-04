import datetime
from storage import database

def log_inventory_change(product_id, quantity_change, reason):
    database.inventory_logs.append({
        'product_id': product_id,
        'quantity_change': quantity_change,
        'reason': reason,
        'timestamp': datetime.datetime.now()
    })
