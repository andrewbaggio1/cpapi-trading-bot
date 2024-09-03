import requests
import json
import urllib3

# ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def orderRequest():
    base_url = "https://localhost:5001/v1/api/"
    account_id = "DU9623668"
    endpoint = f"iserver/account/{account_id}/orders"

    json_body = {
        "orders": [
            {
                "conid": 4815747,  # Nvidia
                "orderType": "MKT",
                "side": "BUY",
                "tif": "DAY",
                "quantity": 100
            }
        ]
    }

    order_req = requests.post(url=base_url + endpoint, verify=False, json=json_body)
    if order_req.status_code == 200:
        order_json = order_req.json()
        print("Order placed successfully:", json.dumps(order_json, indent=2))
    else:
        print("Failed to place order, status code:", order_req.status_code)
        print("Response:", order_req.text)
        return None

def orderReply(replyId):
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "iserver/reply/"
    reply_url = "".join([base_url, endpoint, replyId])

    json_body = {"confirmed": True}

    reply_req = requests.post(url=reply_url, verify=False, json=json_body)
    reply_json = json.dumps(reply_req.json(), indent=2)

    print(reply_req.status_code)
    print(reply_json)

if __name__ == "__main__":
    replyId = orderRequest()
    if replyId:
        orderReply(replyId)