from base64 import b64encode, b64decode
import requests
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# generate keys (in prod I would save these and reuse them)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

bitcoin_prices = []

@app.route('/submit_price', methods=['POST'])
def submit_price():
    data = request.get_json()
    bitcoin_price = data.get('price')
    if bitcoin_price:
        # sign the price and hash in SHA256
        signature = private_key.sign(
            bitcoin_price.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # encode signature to base64 for JSON serialization
        encoded_signature = b64encode(signature).decode('utf-8')

        # store the price and its encoded signature
        bitcoin_prices.append({'price': bitcoin_price, 'signature': encoded_signature})
        
        return jsonify({"message": "Price received and signed", "current_prices": bitcoin_prices}), 200
    else:
        return jsonify({"error": "No price provided"}), 400

@app.route('/verify_price', methods=['POST'])
def verify_price():
    data = request.get_json()
    bitcoin_price = data.get('price')
    encoded_signature = data.get('signature')
    
    if bitcoin_price and encoded_signature:
        # Decode the base64 signature
        signature = b64decode(encoded_signature)
        
        # Verify the signature
        try:
            public_key.verify(
                signature,
                bitcoin_price.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return jsonify({"message": "Signature verified"}), 200
        except Exception as e:
            return jsonify({"error": "Verification failed", "details": str(e)}), 400
    else:
        return jsonify({"error": "No price or signature provided"}), 400

@app.route('/get_prices', methods=['GET'])
def get_prices():
    return jsonify(bitcoin_prices), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/')
def index():
    return app.send_static_file('index.html')
