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

    # Ensure the columns are present and handle potential mismatches
    us2y_col = 'us2y' if 'us2y' in df.columns else None
    us10y_col = 'us10y' if 'us10y' in df.columns else None

    if us2y_col is None or us10y_col is None:
        return jsonify({"error": "Required columns are missing"}), 400

    # Convert to numeric and drop rows with NaN values
    df[us2y_col] = pd.to_numeric(df[us2y_col], errors='coerce')
    df[us10y_col] = pd.to_numeric(df[us10y_col], errors='coerce')
    df = df.dropna(subset=[us2y_col, us10y_col])

    # Get the latest date and corresponding values
    latest_row = df.iloc[-1]
    us2y = latest_row[us2y_col]
    us10y = latest_row[us10y_col]
    spread = us2y - us10y
    asof = latest_row['date']

    # Prepare the response
    response = {
        "us2y": float(us2y),
        "us10y": float(us10y),
        "spread": float(spread),
        "asof": asof
    }
    
    return jsonify(response)

def register(app):
    app.register_blueprint(bp, url_prefix='/rates')
