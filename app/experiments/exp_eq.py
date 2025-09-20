import os
import glob
import pandas as pd
from flask import Blueprint, request, jsonify

bp = Blueprint('eq', __name__)

def register(app):
    app.register_blueprint(bp)

@bp.route('/latest', methods=['GET'])
def latest_prices():
    symbols_param = request.args.get('symbols', default=None)
    if symbols_param:
        symbols = [s.strip() for s in symbols_param.split(',')]
    else:
        symbols = []

    data_files = glob.glob(os.path.join(os.getenv('DATA_DIR', ''), 'bbg_multi_*.xlsx'))
    all_data = []

    for file in data_files:
        df = pd.read_excel(file)
        all_data.append(df)

    combined_data = pd.concat(all_data)
    latest_data = combined_data.groupby('symbol').apply(lambda x: x.nlargest(2, 'date')).reset_index(drop=True)

    results = []
    for symbol in symbols or latest_data['symbol'].unique()[:5]:
        symbol_data = latest_data[latest_data['symbol'] == symbol]
        if len(symbol_data) < 2:
            continue
        
        latest_entry = symbol_data.iloc[0]
        previous_entry = symbol_data.iloc[1]
        
        close = latest_entry['close']
        prev_close = previous_entry['close']
        chg_pct = ((close - prev_close) / prev_close * 100) if prev_close != 0 else None
        
        results.append({
            'symbol': symbol,
            'close': close,
            'chg_pct': chg_pct,
            'asof': latest_entry['date'].strftime('%Y-%m-%d')
        })

    return jsonify({'items': results})
