import requests
import urllib3
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import collections
from iServerMarketScanner import reqIserverScanner

# ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def tickle():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "tickle"

    tickle_req = requests.get(url=base_url + endpoint, verify=False)
    # debugging
    # print("Tickle status code:", tickle_req.status_code)

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

# for graphing
def get_portfolio_value():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "portfolio/DU9623668/positions"
    holdings_req = requests.get(url=base_url + endpoint, verify=False)
    total_value = 0.0
    if holdings_req.status_code == 200:
        holdings = holdings_req.json()
        for item in holdings:
            total_value += item['mktValue']
    return total_value

# initialize variables
short_window = 5  # short-term moving average window
long_window = 20  # long-term moving average window
prices = collections.deque(maxlen=long_window)  # store last prices
position = 0  # track current position (1 for holding, 0 for no position)
max_shares = 1000  # maximum number of shares allowed in the portfolio
portfolio_values = []

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
        return order_json
    else:
        print("Failed to place order, status code:", order_req.status_code)
        print(order_req.text)
        return None

def simple_trading_algorithm():
    global position  # track position state
    market_data = reqIserverScanner()     # fetch market data for Nvidia
    nvidia_data = next((item for item in market_data if item['conid'] == 4815747), None)  # Nvidia's conid

    if not nvidia_data:
        return

    try:
        price = float(nvidia_data['31'])  # convert price to float

        # append the latest price to the prices deque
        prices.append(price)

        # calculate moving averages when there's have enough data
        if len(prices) >= long_window:
            short_ma = sum(list(prices)[-short_window:]) / short_window
            long_ma = sum(prices) / long_window

            current_holdings = get_current_holdings()

            trade_action = 0  # tracks the trade action

            # simple moving average crossover strategy
            if short_ma > long_ma and position == 0 and current_holdings < max_shares:  # buy signal
                quantity = min(10, max_shares - current_holdings)  # don't exceed max_shares
                if quantity > 0:
                    orderRequest(4815747, price, "BUY", quantity)
                    position = 1  # update position to holding
                    trade_action = +10
                    current_holdings += quantity

            elif short_ma < long_ma and position == 1:  # sell signal
                orderRequest(4815747, price, "SELL", 10)
                position = 0  # update position to no position
                trade_action = -10
                current_holdings -= 10

            print(f"{trade_action}, {current_holdings}")  # print trade action and current holdings

    except KeyError as e:
        print(f"Key error: {e}")

def animate(i, portfolio_values):
    portfolio_values.append(get_portfolio_value())
    plt.cla()
    plt.plot(portfolio_values, label="Portfolio Value")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Portfolio Value (USD)")
    plt.title("Portfolio Value Over Time")
    plt.legend()
    plt.grid(True)

if __name__ == "__main__":
    start_time = time.time()
    #fig = plt.figure()
    #ani = animation.FuncAnimation(fig, animate, fargs=(portfolio_values,), interval=1000, cache_frame_data=False)
    #plt.show(block=False)
    while True:
        try:
            for _ in range(10):
                tickle()
                simple_trading_algorithm()
                # portfolio_values.append(get_portfolio_value())
                time.sleep(0.1)  # run the trading algorithm every 0.1 seconds
            # plt.pause(0.1) # pause for 0.1 seconds to update the plot
            time.sleep(max(0, 1 - (time.time() - start_time)))
            start_time = time.time()
        except Exception as e:
            print("Error in trading bot:", str(e))