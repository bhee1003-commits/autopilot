from flask import Blueprint, request, jsonify
import pandas as pd
import glob
import os

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

    result_items = []
    for symbol in symbols or latest_data['symbol'].unique()[:5]:
        symbol_data = latest_data[latest_data['symbol'] == symbol]
        if len(symbol_data) < 2:
            continue
        
        latest_close = symbol_data.iloc[0]['close']
        prev_close = symbol_data.iloc[1]['close']
        chg_pct = ((latest_close - prev_close) / prev_close * 100) if prev_close != 0 else None
        
        result_items.append({
            'symbol': symbol,
            'close': latest_close,
            'chg_pct': chg_pct,
            'asof': symbol_data.iloc[0]['date'].strftime('%Y-%m-%d')
        })

    return jsonify({'items': result_items})
