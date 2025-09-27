import os
import pandas as pd
from flask import Blueprint, jsonify

bp = Blueprint('rates', __name__)

def register(app):
    app.register_blueprint(bp, url_prefix='/rates')

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
        return jsonify({"error": "Required columns not found"}), 400

    # Convert to numeric and handle errors
    df[us2y_col] = pd.to_numeric(df[us2y_col], errors='coerce')
    df[us10y_col] = pd.to_numeric(df[us10y_col], errors='coerce')

    # Drop rows with NaN values
    df = df.dropna(subset=[us2y_col, us10y_col])

    # Get the latest date and corresponding values
    latest_row = df.iloc[-1]
    us2y = latest_row[us2y_col]
    us10y = latest_row[us10y_col]
    asof = latest_row['date']

    # Calculate spread
    spread = us2y - us10y

    # Prepare the response
    response = {
        "us2y": float(us2y),
        "us10y": float(us10y),
        "spread": float(spread),
        "asof": asof
    }

    return jsonify(response)
