from flask import Blueprint, request, jsonify
import pandas as pd
import os

bp = Blueprint('commo', __name__)

# Ticker to label mapping
TICKER_LABEL_MAP = {
    "CL1": "CL1 Comdty",
    "XAU": "XAU Curncy"
}

def load_data(tickers):
    data = []
    for ticker in tickers:
        # Simulate loading data from Excel files
        # In a real scenario, you would read from the actual files
        # Here we just mock the last price and asof date
        last_price = 100.0 if ticker in TICKER_LABEL_MAP else 0.0  # Mock last price
        asof_date = "2023-10-01"  # Mock date
        if last_price > 0:
            data.append({"ticker": ticker, "last": last_price, "asof": asof_date})
    return data

@bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers_param = request.args.get('tickers', '')
    tickers = tickers_param.split(',')
    items = load_data(tickers)
    
    return jsonify({"items": items})

def register(app):
    app.register_blueprint(bp, url_prefix='/commo')
