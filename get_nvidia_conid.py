import requests
import urllib3
import json

# ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_nvidia_conid():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "iserver/secdef/search"
    search_body = {
        "symbol": "NVDA",
        "secType": "STK"
    }

    search_req = requests.post(url=base_url + endpoint, verify=False, json=search_body)
    if search_req.status_code == 200:
        search_results = search_req.json()
        for result in search_results:
            if result.get('symbol') == 'NVDA' and result.get('exchange') == 'NASDAQ':
                return result.get('conid')
    else:
        print("Failed to fetch conid, status code:", search_req.status_code)
        return None

nvidia_conid = get_nvidia_conid()
print(f"Nvidia conid: {nvidia_conid}")