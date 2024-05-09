import requests

def fetch_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    
    try:
        # HTTP GET request to the API
        response = requests.get(url)

        # raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # get response as json
        data = response.json()
        
        # accessing the 'rate' field under 'USD' in 'bpi'
        bitcoin_price = data['bpi']['USD']['rate']
        
        print(f"Current Bitcoin price (USD): {bitcoin_price}")
        return bitcoin_price
    
    except requests.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")

def fetch_and_send_bitcoin_price():
    api_endpoint = "http://localhost:5000/submit_price"

    try:
        bitcoin_price = fetch_bitcoin_price()

        # Send the price to our Flask API
        send_response = requests.post(api_endpoint, json={"price": bitcoin_price})
        send_response.raise_for_status()

        print("Price sent successfully:", bitcoin_price)
    except requests.RequestException as e:
        print("Error:", e)

fetch_and_send_bitcoin_price()
fetch_bitcoin_price()
