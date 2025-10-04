import os
import pandas as pd
from flask import Blueprint, jsonify

bp = Blueprint('rates', __name__)

@bp.route('/yieldcurve', methods=['GET'])
def yield_curve():
    data_dir = os.environ.get("DATA_DIR", "data")
    file_path = os.path.join(data_dir, 'exog_with_labels_fixed.csv')
    
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Ensure the columns are present and handle potential mismatches
    if 'us2y' not in df.columns or 'us10y' not in df.columns:
        return jsonify({"error": "Required columns are missing"}), 400

    # Convert to numeric, handling errors and missing values
    df['us2y'] = pd.to_numeric(df['us2y'], errors='coerce')
    df['us10y'] = pd.to_numeric(df['us10y'], errors='coerce')

    # Drop rows with NaN values in the relevant columns
    df = df.dropna(subset=['us2y', 'us10y'])

    # Get the latest date and corresponding values
    latest_row = df.iloc[-1]
    us2y = latest_row['us2y']
    us10y = latest_row['us10y']
    asof = latest_row['date']
    spread = us2y - us10y

    # Create the response
    response = {
        "us2y": float(us2y),
        "us10y": float(us10y),
        "spread": float(spread),
        "asof": asof
    }
    
    return jsonify(response)

def register(app):
    app.register_blueprint(bp, url_prefix='/rates')
