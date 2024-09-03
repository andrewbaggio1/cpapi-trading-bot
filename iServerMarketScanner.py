import requests
import urllib3
import json

# ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def reqIserverScanner():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "iserver/marketdata/snapshot"
    
    # Nvidia conid
    conid = "4815747"
    
    params = {
        "conids": conid,
        "fields": "31"  # 31 corresponds to the last price
    }

    market_data_req = requests.get(url=base_url + endpoint, verify=False, params=params)
    if market_data_req.status_code == 200:
        response_json = market_data_req.json()
        return response_json
    else:
        print("Failed to fetch market data, status code:", market_data_req.status_code)
        return []

if __name__ == "__main__":
    data = reqIserverScanner()