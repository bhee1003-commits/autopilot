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
        symbols = []

    data_dir = os.getenv('DATA_DIR', './')  # Default to current directory if DATA_DIR is not set
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))
    
    all_data = []
    for file in files:
        df = pd.read_excel(file)
        all_data.append(df)

    if all_data:
        combined_data = pd.concat(all_data)
        latest_data = combined_data.groupby('symbol').apply(lambda x: x.nlargest(2, 'date')).reset_index(drop=True)

        results = []
        for symbol in symbols:
            symbol_data = latest_data[latest_data['symbol'].str.lower() == symbol.lower()]
            if len(symbol_data) == 2:
                close = symbol_data.iloc[0]['close']
                prev_close = symbol_data.iloc[1]['close']
                chg_pct = ((close - prev_close) / prev_close) * 100
                results.append({
                    'symbol': symbol,
                    'close': close,
                    'chg_pct': chg_pct,
                    'asof': symbol_data.iloc[0]['date'].strftime('%Y-%m-%d')
                })

        if not results and not symbols:
            # If no symbols were provided, return top 5 by latest close
            top_results = latest_data.nlargest(5, 'close')
            for _, row in top_results.iterrows():
                results.append({
                    'symbol': row['symbol'],
                    'close': row['close'],
                    'chg_pct': None,  # Cannot calculate without previous close
                    'asof': row['date'].strftime('%Y-%m-%d')
                })

        return jsonify({'items': results}), 200

    return jsonify({'items': []}), 200
