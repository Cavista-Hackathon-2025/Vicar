from flask import Flask, request, jsonify
from  flask_cors import CORS
from db import init_db, update_stock, get_stock
from utils import calculate_forecast, check_counterfeit, send_sms
import os

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/api/update', methods=['POST'])
def update():
    data = request.get_json()
    drug = data['drug']
    units_left = int(data['units_left'])
    restock_at = int(data['restock_at'])
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


@app.route('/api/stock', methods=['GET'])
def stock():
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
    return jsonify({"inventory":inventory})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False) #Debug mode is false in production



    #app.run(host='0.0.0.0', port=5000, debug=True)
