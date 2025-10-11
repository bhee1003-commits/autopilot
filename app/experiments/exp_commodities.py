from flask import Blueprint, request, jsonify
import pandas as pd
import os

bp = Blueprint('commo', __name__)

# Ticker to label mapping
TICKER_LABEL_MAP = {
    "CL1": "CL1 Comdty",
    "XAU": "XAU Curncy"
}

def get_snapshot(tickers):
    data_dir = os.getenv('DATA_DIR', '')
    snapshots = []
    
    for ticker in tickers:
        label = TICKER_LABEL_MAP.get(ticker)
        if label:
            # Simulate reading from an Excel file
            file_path = os.path.join(data_dir, f'bbg_multi_{ticker}.xlsx')
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                # Assuming the last price and asof date are in the DataFrame
                last_price = df['last'].iloc[-1]  # Get the last price
                asof_date = df['asof'].iloc[-1]    # Get the asof date
                snapshots.append({"ticker": ticker, "last": last_price, "asof": asof_date})

    return snapshots

@bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers = request.args.get('tickers', '').split(',')
    items = get_snapshot(tickers)
    
    return jsonify({"items": items})

def register(app):
    app.register_blueprint(bp, url_prefix='/commo')
