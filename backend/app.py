from flask import Flask, request, jsonify
from flask_cors import CORS  
from db import init_db, init_test_data, update_stock, get_stock
from utils import calculate_forecast, check_counterfeit, send_sms
import os
from pyngrok import ngrok  # Add ngrok support
import logging
from werkzeug.exceptions import BadRequest

# Add logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize database and test data
init_db()
init_test_data()

# Setup ngrok tunnel
def setup_ngrok():
    try:
        # Get public URL
        public_url = ngrok.connect(5000).public_url
        print(f"* ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")
        app.config["BASE_URL"] = public_url
    except Exception as e:
        print(f"Failed to setup ngrok: {e}")

@app.route('/api/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['drug', 'units_left', 'restock_at']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        drug = data['drug']
        try:
            units_left = int(data['units_left'])
            restock_at = int(data['restock_at'])
        except ValueError:
            return jsonify({"error": "units_left and restock_at must be numbers"}), 400

        batch_number = data.get('batch_number', "")

        last_updated, initial_units = update_stock(drug, units_left, restock_at, batch_number)
        forecast = calculate_forecast(drug, units_left, restock_at, last_updated, initial_units)
        is_valid = check_counterfeit(batch_number) if batch_number else True

        message_parts = []
        if units_left <= restock_at:
            message_parts.append(f"Only {units_left} {drug} left, order {forecast} soon!")
            if not is_valid and batch_number:
                message_parts.append(f"WARNING: Batch {batch_number} looks fake.")
            if message_parts:
                send_sms(" ".join(message_parts))

        return jsonify({
            "status": "success",
            "drug": drug,
            "units_left": units_left,
            "restock_at": restock_at,
            "forecast": forecast,
            "batch_number": batch_number,
            "counterfeit_risk": not is_valid
        })
    except Exception as e:
        logger.error(f"Error in update endpoint: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/stock', methods=['GET'])
def stock():
    try:
        rows = get_stock()
        inventory = [
            {
                "drug": r[0],
                "units_left": r[1],
                "restock_at": r[2],
                "forecast": calculate_forecast(r[0], r[1], r[2], r[3], r[4]),
                "batch_number": r[5] or "N/A",
                "counterfeit_risk": not check_counterfeit(r[5]) if r[5] else False
            } for r in rows
        ]
        return jsonify({"inventory": inventory})
    except Exception as e:
        logger.error(f"Error in stock endpoint: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to Pharmacy Inventory API",
        "endpoints": {
            "GET /api/stock": "Get all inventory items",
            "POST /api/update": "Update inventory item"
        }
    })

# Add error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "details": str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "details": str(error)}), 500

if __name__ == "__main__":
    # Development settings
    port = int(os.getenv("PORT", 5000))
    
    if os.getenv("USE_NGROK", "False") == "True":
        setup_ngrok()
    
    app.run(
        host='127.0.0.1',  # Change to localhost
        port=port,
        debug=True  # Enable debug mode for development
    )
