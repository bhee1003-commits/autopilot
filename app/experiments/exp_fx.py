from flask import Blueprint, jsonify
import pandas as pd
import glob
import os

fx_bp = Blueprint('fx', __name__)

def register(app):
    app.register_blueprint(fx_bp)

@fx_bp.route('/dxy', methods=['GET'])
def get_dxy():
    data_dir = os.getenv('DATA_DIR', './data')  # Default to './data' if DATA_DIR is not set
    files = glob.glob(os.path.join(data_dir, 'bbg_multi_*.xlsx'))
    
    if not files:
        return jsonify({"error": "No data files found"}), 404

    dxy_data = []
    
    for file in files:
        xls = pd.ExcelFile(file)
        for sheet_name in xls.sheet_names:
            if 'DXY' in sheet_name or 'Index' in sheet_name:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                if 'DXY' in df.columns:
                    dxy_data.append(df[['DXY', 'Timestamp']])  # Assuming 'Timestamp' column exists

    if not dxy_data:
        return jsonify({"error": "No DXY data found"}), 404

    combined_df = pd.concat(dxy_data)
    latest_row = combined_df.loc[combined_df['Timestamp'].idxmax()]
    
    response = {
        "dxy": latest_row['DXY'],
        "ts": latest_row['Timestamp'].isoformat()
    }
    
    return jsonify(response)
