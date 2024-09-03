import requests
import json

# disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def orderReply():
    base_url = "https://localhost:5001/v1/api/"
    endpoint = "iserver/reply/"
    replyId = "e554837f-eb56-4a6f-8930-a9ce67e74b6c"

    reply_url = "".join([base_url, endpoint, replyId])

    json_body = {"confirmed":True}
 
    reply_req = requests.post(url=reply_url, verify=False, json=json_body)
    reply_json = json.dumps(reply_req.json(), indent=2)

    print(reply_req.status_code)
    print(reply_json)
    
if __name__ == "__main__":
    orderReply()