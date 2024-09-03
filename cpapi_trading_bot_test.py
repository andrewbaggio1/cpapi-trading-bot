import requests
import json
import time
import collections
from iServerMarketScanner import reqIserverScanner

# ignore insecure error messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tickle():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "tickle"

    tickle_req = requests.get(url=base_url + endpoint, verify=False)
    print("Tickle status code:", tickle_req.status_code)

def get_current_holdings():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "portfolio/DU9623668/positions"

    holdings_req = requests.get(url=base_url + endpoint, verify=False)
    if holdings_req.status_code == 200:
        holdings = holdings_req.json()
        nvidia_holding = next((item for item in holdings if item["conid"] == 4815747), None)  # Nvidia conid
        if nvidia_holding:
            return nvidia_holding['position']
    return 0

# initialize variables
short_window = 5  # short-term moving average window
long_window = 20  # long-term moving average window
prices = collections.deque(maxlen=long_window)  # store last 'long_window' prices
position = 0  # track current position (1 for holding, 0 for no position)
max_shares = 1000  # maximum number of shares allowed in the portfolio

def orderRequest(conid, price, side, quantity):
    base_url = "https://localhost:5001/v1/api/"
    account_id = "DU9623668"
    endpoint = f"iserver/account/{account_id}/orders"

    json_body = {
        "orders": [
            {
                "conid": conid,
                "orderType": "MKT",
                "side": side,
                "tif": "DAY",
                "quantity": quantity
            }
        ]
    }

    order_req = requests.post(url=base_url + endpoint, verify=False, json=json_body)
    if order_req.status_code == 200:
        order_json = order_req.json()
        print(f"Order placed successfully: {side} {quantity} shares of conid {conid}")
        print(json.dumps(order_json, indent=2))
        return order_json
    else:
        print("Failed to place order, status code:", order_req.status_code)
        print("Response:", order_req.text)
        return None

def simple_trading_algorithm():
    global position  # use global variable to track position state
    # fetch market data for Nvidia
    market_data = reqIserverScanner()
    nvidia_data = next((item for item in market_data if item['conid'] == 4815747), None)  # Nvidia's conid

    if not nvidia_data:
        print("Failed to fetch Nvidia market data")
        return

    try:
        price = float(nvidia_data['31'])  # convert price to float
        print(f"Current price: {price}")  # debugging print

        # append the latest price to the prices deque
        prices.append(price)
        print(f"Updated prices deque: {list(prices)}")  # debugging print

        # calculate moving averages if we have enough data
        if len(prices) >= long_window:
            short_ma = sum(list(prices)[-short_window:]) / short_window
            long_ma = sum(prices) / long_window

            print(f"Short MA: {short_ma}, Long MA: {long_ma}")  # debugging print

            current_holdings = get_current_holdings()
            print(f"Current Nvidia holdings: {current_holdings}")  # debugging print

            # simple moving average crossover strategy
            if short_ma > long_ma and position == 0 and current_holdings < max_shares:  # buy signal
                quantity = min(10, max_shares - current_holdings)  # don't exceed max_shares
                if quantity > 0:
                    print(f"Buy signal detected: Short MA ({short_ma}) > Long MA ({long_ma})")
                    orderRequest(4815747, price, "BUY", quantity)
                    position = 1  # update position to holding
                    print(f"Bought {quantity} shares of Nvidia stock")
                    print(f"Total Nvidia stock in portfolio: {current_holdings + quantity} shares")

            elif short_ma < long_ma and position == 1:  # sell signal
                print(f"Sell signal detected: Short MA ({short_ma}) < Long MA ({long_ma})")
                orderRequest(4815747, price, "SELL", 10)
                position = 0  # update position to no position
                print(f"Sold 10 shares of Nvidia stock")
                print(f"Total Nvidia stock in portfolio: {current_holdings - 10} shares")

    except KeyError as e:
        print(f"Key error: {e}")

if __name__ == "__main__":
    while True:
        try:
            tickle()
            simple_trading_algorithm()
            time.sleep(1)  # run the trading algorithm every 1 second
        except Exception as e:
            print("Error in trading bot:", str(e))