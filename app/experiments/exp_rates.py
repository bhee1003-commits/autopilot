import os
import pandas as pd
from flask import Blueprint, jsonify

bp = Blueprint('rates', __name__)

@bp.route('/yieldcurve', methods=['GET'])
def yield_curve():
    data_dir = os.environ.get("DATA_DIR", "data")
    file_path = os.path.join(data_dir, "exog_with_labels_fixed.csv")
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure the columns are present and handle potential type issues
    df['us2y'] = pd.to_numeric(df['us2y'], errors='coerce')
    df['us10y'] = pd.to_numeric(df['us10y'], errors='coerce')
    
    # Drop rows with NaN values in us2y or us10y
    df = df.dropna(subset=['us2y', 'us10y'])
    
    # Get the most recent date
    latest_row = df.iloc[-1]
    asof_date = latest_row['date']
    us2y = latest_row['us2y']
    us10y = latest_row['us10y']
    spread = us2y - us10y
    
    # Prepare the response
    response = {
        "us2y": float(us2y),
        "us10y": float(us10y),
        "spread": float(spread),
        "asof": asof_date
    }
    
    return jsonify(response)

def register(app):
    app.register_blueprint(bp, url_prefix='/rates')
