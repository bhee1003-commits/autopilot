from flask import Blueprint, jsonify
import pandas as pd
import glob
import os

bp = Blueprint('fx', __name__)

def get_latest_dxy(data_dir):
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))
    latest_dxy = None
    latest_ts = None

    for file in files:
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if 'DXY' in df.columns or 'Index' in df.columns:
                # Assuming the DXY values are in a column named 'DXY' or 'Index'
                dxy_col = 'DXY' if 'DXY' in df.columns else 'Index'
                latest_row = df.iloc[-1]  # Get the latest row
                dxy_value = latest_row[dxy_col]
                ts_value = latest_row['Timestamp'] if 'Timestamp' in df.columns else None
                
                if latest_dxy is None or (ts_value and ts_value > latest_ts):
                    latest_dxy = dxy_value
                    latest_ts = ts_value

    return latest_dxy, latest_ts

@bp.route('/dxy', methods=['GET'])
def dxy():
    data_dir = os.getenv('DATA_DIR', './data')  # Default to './data' if not set
    dxy_value, ts_value = get_latest_dxy(data_dir)

    if dxy_value is not None and ts_value is not None:
        return jsonify({"dxy": float(dxy_value), "ts": ts_value.isoformat()}), 200
    else:
        return jsonify({"error": "No data found"}), 404

def register(app):
    app.register_blueprint(bp, url_prefix='/fx')
