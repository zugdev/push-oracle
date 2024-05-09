from flask import Flask, request, jsonify

app = Flask(__name__)

bitcoin_prices = []

@app.route('/submit_price', methods=['POST'])
def submit_price():
    data = request.get_json()
    bitcoin_price = data.get('price')
    if bitcoin_price:
        bitcoin_prices.append(bitcoin_price)
        return jsonify({"message": "Price received", "current_prices": bitcoin_prices}), 200
    else:
        return jsonify({"error": "No price provided"}), 400

@app.route('/get_prices', methods=['GET'])
def get_prices():
    return jsonify({"current_prices": bitcoin_prices}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
