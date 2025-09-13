from flask import Blueprint, request, jsonify
import pandas as pd
import os
from datetime import datetime

commo_bp = Blueprint('commo', __name__)

# Ticker to label mapping
TICKER_LABEL_MAP = {
    "CL1": "CL1 Comdty",
    "XAU": "XAU Curncy"
}

def get_snapshot(tickers):
    data_dir = os.getenv('DATA_DIR', './data')
    snapshots = []
    
    for ticker in tickers:
        # Simulate reading from Excel files
        # In a real implementation, you would read the actual data
        # Here we just create dummy data for demonstration
        last_price = 100.0  # Dummy last price
        asof_date = datetime.now().strftime('%Y-%m-%d')  # Current date as 'asof'
        
        if ticker in TICKER_LABEL_MAP:
            snapshots.append({
                "ticker": ticker,
                "last": last_price,
                "asof": asof_date
            })
    
    return snapshots

@commo_bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers_param = request.args.get('tickers', '')
    tickers = tickers_param.split(',')
    
    items = get_snapshot(tickers)
    
    return jsonify({"items": items})

def register(app):
    app.register_blueprint(commo_bp, url_prefix='/commo')
