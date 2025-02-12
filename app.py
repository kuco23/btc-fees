from flask import Flask, jsonify, request
from analyse import get_data

btc_precision = 1e8

app = Flask(__name__)

# Route for a simple GET request
@app.route('/btc-fees', methods=['GET'])
def home():
    fee = request.args.get('redemption_fee')
    lot_size = request.args.get('lot_size')
    perc = request.args.get('perc') or 90
    data = get_data(int(btc_precision * float(lot_size)), float(fee), int(perc))
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask server on localhost and port 5000
    app.run(host='0.0.0.0', port=9600, debug=True)