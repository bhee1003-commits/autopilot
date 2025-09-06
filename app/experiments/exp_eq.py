from flask import Blueprint, request, jsonify
import pandas as pd
import glob
import os

bp = Blueprint('eq', __name__)

def register(app):
    app.register_blueprint(bp, url_prefix='/eq')

@bp.route('/latest', methods=['GET'])
def latest_prices():
    symbols_param = request.args.get('symbols', default=None)
    if symbols_param:
        symbols = [s.strip() for s in symbols_param.split(',')]
    else:
        symbols = None

    data_dir = os.getenv('DATA_DIR', './')  # Default to current directory if DATA_DIR is not set
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))

    all_data = []
    for file in files:
        df = pd.read_excel(file)
        all_data.append(df)

    merged_data = pd.concat(all_data)
    latest_data = merged_data.groupby('symbol').apply(lambda x: x.nlargest(2, 'date')).reset_index(drop=True)

    results = []
    for symbol in latest_data['symbol'].unique():
        symbol_data = latest_data[latest_data['symbol'] == symbol]
        if len(symbol_data) < 2:
            continue
        
        latest_entry = symbol_data.iloc[0]
        previous_entry = symbol_data.iloc[1]
        
        close = latest_entry['close']
        prev_close = previous_entry['close']
        chg_pct = ((close - prev_close) / prev_close) * 100 if prev_close != 0 else None
        
        results.append({
            'symbol': symbol,
            'close': close,
            'chg_pct': chg_pct,
            'asof': latest_entry['date'].strftime('%Y-%m-%d')
        })

    if symbols:
        results = [item for item in results if item['symbol'] in symbols]

    results = results[:5]  # Limit to top 5 if symbols are specified

    return jsonify({'items': results})
