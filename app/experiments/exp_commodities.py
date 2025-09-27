from flask import Blueprint, request, jsonify
import pandas as pd
import os

commo_bp = Blueprint('commo', __name__)

# Ticker to label mapping
TICKER_LABEL_MAP = {
    "CL1": "CL1 Comdty",
    "XAU": "XAU Curncy"
}

def get_snapshot(tickers):
    data_dir = os.getenv('DATA_DIR', '')
    items = []
    
    for ticker in tickers:
        label = TICKER_LABEL_MAP.get(ticker)
        if label:
            # Simulate reading from an Excel file
            # In a real implementation, you would read the actual data
            # For this example, we will just create dummy data
            last = 100.0  # Dummy value for last price
            asof = "2023-10-01"  # Dummy date
            items.append({"ticker": ticker, "last": last, "asof": asof})
    
    return items

@commo_bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers_param = request.args.get('tickers', '')
    tickers = tickers_param.split(',')
    items = get_snapshot(tickers)
    
    return jsonify({"items": items})

def register(app):
    app.register_blueprint(commo_bp, url_prefix='/commo')
