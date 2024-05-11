from base64 import b64encode, b64decode
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from web3 import Web3
import json

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545')) # default anvil eth node

# check rpc connection
if not w3.is_connected():
    raise Exception("Failed to connect to node.")

contract_json_path = 'static/PriceFeed.json'

with open(contract_json_path, 'r') as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']  

contract_address = "0x34A1D3fff3958843C43aD80F30b94c510645C316"

contract = w3.eth.contract(address=contract_address.strip(), abi=contract_abi)

# generate keys (replicate notarizing)
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
        timestamp = datetime.now().isoformat()

        # append to local storage
        bitcoin_prices.append({'price': bitcoin_price, 'signature': encoded_signature, 'timestamp': timestamp})

        # submit to chain
        cleaned_price = bitcoin_price.replace(',', '')
        tx_hash = contract.functions.submitPrice(
            'BTC',
            int(float(cleaned_price) * 100), 
            int(datetime.now().timestamp())
        ).transact({'from': w3.eth.accounts[0], 'gas': 500000})

        # wait for tx to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({"message": "Price received and signed, submitted to blockchain", "tx_receipt": tx_receipt.transactionHash.hex(), "current_prices": bitcoin_prices}), 200
    else:
        return jsonify({"error": "No price provided"}), 400

@app.route('/verify_price', methods=['POST'])
def verify_price():
    data = request.get_json()
    bitcoin_price = data.get('price')
    encoded_signature = data.get('signature')
    timestamp = data.get('timestamp')  
    
    if bitcoin_price and encoded_signature:
        signature = b64decode(encoded_signature)
        
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
            return jsonify({"message": "Signature verified", "timestamp": timestamp}), 200
        except Exception as e:
            return jsonify({"error": "Verification failed", "details": str(e), "timestamp": timestamp}), 400
    else:
        return jsonify({"error": "No price or signature provided"}), 400

@app.route('/get_prices', methods=['GET'])
def get_prices():
    return jsonify(bitcoin_prices), 200

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)