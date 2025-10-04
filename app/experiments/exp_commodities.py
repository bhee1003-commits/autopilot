from flask import Blueprint, request, jsonify
import pandas as pd
import glob
import os

bp = Blueprint('commo', __name__)

# Ticker to label mapping
TICKER_LABEL_MAP = {
    "CL1": "CL1 Comdty",
    "XAU": "XAU Curncy"
}

def load_data():
    data_dir = os.getenv('DATA_DIR', './')
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))
    data = {}
    
    for file in files:
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            ticker = row.get('Ticker')
            last = row.get('Last')
            asof = row.get('Asof')
            if ticker and last is not None and asof:
                data[ticker] = {'last': last, 'asof': asof}
    
    return data

@bp.route('/snapshot', methods=['GET'])
def snapshot():
    tickers = request.args.get('tickers', '').split(',')
    data = load_data()
    
    items = []
    for ticker in tickers:
        if ticker in data:
            items.append({"ticker": ticker, "last": data[ticker]['last'], "asof": data[ticker]['asof']})
    
    return jsonify({"items": items})

def register(app):
    app.register_blueprint(bp, url_prefix='/commo')
