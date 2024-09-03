import requests
import urllib3

# ignore insecure error messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_current_holdings():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "portfolio/DU9623668/positions"

    holdings_req = requests.get(url=base_url + endpoint, verify=False)
    if holdings_req.status_code == 200:
        holdings = holdings_req.json()
        print("Holdings:", holdings)  # print for debugging
        return holdings
    else:
        print("Failed to fetch holdings, status code:", holdings_req.status_code)
        return None

if __name__ == "__main__":
    holdings = get_current_holdings()