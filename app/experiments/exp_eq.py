import os
import glob
import pandas as pd
from flask import Blueprint, request, jsonify

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

    data_files = glob.glob(os.path.join(os.getenv('DATA_DIR', ''), 'bbg_multi_*.xlsx'))
    all_data = []

    for file in data_files:
        df = pd.read_excel(file)
        all_data.append(df)

    combined_data = pd.concat(all_data, ignore_index=True)
    latest_data = combined_data.groupby('symbol').apply(lambda x: x.nlargest(2, 'date')).reset_index(drop=True)

    results = []
    for symbol in (latest_data['symbol'].unique() if symbols is None else symbols):
        symbol_data = latest_data[latest_data['symbol'] == symbol]
        if len(symbol_data) < 2:
            continue

        latest_row = symbol_data.iloc[0]
        previous_row = symbol_data.iloc[1]
        close = latest_row['close']
        prev_close = previous_row['close']
        chg_pct = ((close - prev_close) / prev_close * 100) if prev_close != 0 else None

        results.append({
            'symbol': symbol,
            'close': close,
            'chg_pct': chg_pct,
            'asof': latest_row['date'].strftime('%Y-%m-%d')
        })

    if symbols and len(results) != len(symbols):
        return jsonify({'error': 'Requested symbols not found'}), 404

    return jsonify({'items': results})
