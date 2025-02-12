from flask import Flask, jsonify, request
from analyse import get_data

btc_precision = 1e8

app = Flask(__name__)

# Route for a simple GET request
@app.route('/btc-fees', methods=['GET'])
def home():
    fee = request.args.get('redemption_fee')
    lot_size = request.args.get('lot_size')
    perc = int(request.args.get('perc') or 50)
    if fee is None or lot_size is None or perc not in [10, 25, 50]:
        return jsonify({'error': 'Please provide redemption_fee and lot_size and perc 10, 25 or 50'})
    data = get_data(int(btc_precision * float(lot_size)), float(fee), perc)
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask server on localhost and port 5000
    app.run(host='0.0.0.0', port=9600, debug=True)