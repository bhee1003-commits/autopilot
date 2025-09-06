from flask import Blueprint, jsonify
import pandas as pd
import glob
import os

bp = Blueprint('fx', __name__)

def register(app):
    app.register_blueprint(bp, url_prefix='/fx')

@bp.route('/dxy', methods=['GET'])
def get_dxy():
    data_dir = os.getenv('DATA_DIR', './data')  # Default to './data' if DATA_DIR is not set
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))
    
    if not files:
        return jsonify({"error": "No data files found"}), 404
    
    dxy_data = []
    
    for file in files:
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            if 'DXY' in df.columns or 'Index' in df.columns:
                dxy_data.append(df[['DXY', 'Timestamp']])  # Assuming 'Timestamp' is the column name for time
    
    if not dxy_data:
        return jsonify({"error": "No DXY data found"}), 404
    
    combined_df = pd.concat(dxy_data)
    latest_row = combined_df.loc[combined_df['Timestamp'].idxmax()]
    
    response = {
        "dxy": latest_row['DXY'],
        "ts": latest_row['Timestamp'].isoformat()
    }
    
    return jsonify(response)
