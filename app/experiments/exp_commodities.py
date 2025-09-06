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
    data_dir = os.getenv('DATA_DIR', '')
    data_files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx')]
    snapshots = []

    for file in data_files:
        file_path = os.path.join(data_dir, file)
        df = pd.read_excel(file_path)

        for ticker in tickers:
            if ticker in df['Ticker'].values:
                last_row = df[df['Ticker'] == ticker].iloc[-1]
                snapshots.append({
                    "ticker": ticker,
                    "last": last_row['Last'],
                    "asof": last_row['Date'].strftime('%Y-%m-%d')
                })

    return snapshots

@bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers_param = request.args.get('tickers', '')
    tickers = tickers_param.split(',')

    # Load data for the requested tickers
    items = load_data(tickers)

    # Filter items to match requested tickers
    items = [item for item in items if item['ticker'] in tickers]

    return jsonify({"items": items})

def register(app):
    app.register_blueprint(bp, url_prefix='/commo')
