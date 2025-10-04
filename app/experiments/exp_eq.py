import os
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
        symbols = []

    data_dir = os.getenv('DATA_DIR', '')
    files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx') and 'bbg_multi_' in f]
    
    all_data = []
    
    for file in files:
        file_path = os.path.join(data_dir, file)
        df = pd.read_excel(file_path)
        all_data.append(df)

    combined_data = pd.concat(all_data)
    
    # Assuming the DataFrame has 'symbol', 'close', and 'date' columns
    latest_data = combined_data.groupby('symbol').apply(lambda x: x.nlargest(2, 'date')).reset_index(drop=True)

    results = []
    
    for symbol in symbols:
        symbol_data = latest_data[latest_data['symbol'].str.contains(symbol, case=False, regex=True)]
        
        if len(symbol_data) >= 2:
            latest_close = symbol_data.iloc[0]['close']
            prev_close = symbol_data.iloc[1]['close']
            chg_pct = ((latest_close - prev_close) / prev_close) * 100
            
            results.append({
                'symbol': symbol_data.iloc[0]['symbol'],
                'close': latest_close,
                'chg_pct': chg_pct,
                'asof': symbol_data.iloc[0]['date'].strftime('%Y-%m-%d')
            })

    # If no symbols were provided, return the top 5 results
    if not symbols:
        results = results[:5]

    return jsonify({'items': results})
