from flask import Flask, request, render_template, redirect, url_for
from db import init_db, update_stock, get_stock
from utils import calculate_forecast, check_counterfeit, send_sms

app = Flask(__name__)

init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        drug = request.form['drug']
        units_left = int(request.form['units_left'])
        restock_at = int(request.form['restock_at'])
        batch_number = request.form.get('batch_number', "")

        last_updated, initial_units = update_stock(drug, units_left, restock_at, batch_number)
        forecast = calculate_forecast(drug, units_left, restock_at, last_updated, initial_units)
        is_valid = check_counterfeit(batch_number) if batch_number else True

        message_parts = []
        if units_left <= restock_at:
            message_parts.append(f"Only{units_left} {drug} left, order {forecast} soon!")
            if not is_valid and batch_number:
                message_parts.append(f"WARNING:Batch {batch_number} looks fake.")
            if message_parts:
                send_sms(" ".join(message_parts))
                return redirect(url_for('stock'))
        return render_template('index.html')

@app.route('/stock')
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
    return render_template('stock.html', inventory=inventory)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
