import requests
import urllib3

# disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def orderRequest(conid, action, quantity):
    base_url = "https://localhost:5001/v1/api/"
    account_id = "DU9623668"  # Replace with your account ID if different
    endpoint = f"iserver/account/{account_id}/orders"

    order_payload = {
        "conid": conid,
        "secType": "STK",
        "orderType": "MKT",
        "action": action,
        "totalQuantity": quantity,
        "account": account_id
    }

    order_req = requests.post(url=base_url + endpoint, verify=False, json=order_payload)
    if order_req.status_code == 200:
        print("Order placed successfully:", order_req.json())
    else:
        print(f"Failed to place order, status code: {order_req.status_code}")
        print("Response:", order_req.text)

def buy_nvidia_shares():
    # Nvidia conid
    conid = 4815747
    # Quantity to buy
    quantity = 1000
    # Place a buy order
    orderRequest(conid, "BUY", quantity)

if __name__ == "__main__":
    buy_nvidia_shares()