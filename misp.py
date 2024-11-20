import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

misp_token = "<YOUR_MISP_API_TOKEN>"
misp_event_id = "<YOUR_MISP_EVENT_ID>"
misp_api_url = f"https://<YOUR_MISP_URL>/attributes/add/{misp_event_id}"
publish_url = f"https://<YOUR_MISP_URL>/events/publish/{misp_event_id}"

misp_headers = {
    "Authorization": misp_token,
    "Accept": "application/json"
}

def add_attribute_to_existing_event(approved_ips_and_urls):
    for ip, url in approved_ips_and_urls:
        attribute_data = {
            "category": "Network activity",
            "type": "ip-src",
            "value": ip,
            "to_ids": True,
            "comment": url
        }
        
        try:
            response = requests.post(misp_api_url, headers=misp_headers, json=attribute_data, verify=False)

            print(f"Response Status Code: {response.status_code}")

            if response.status_code == 200:
                print(f"Attribute added successfully to MISP event ID {misp_event_id} for IP: {ip} and URL: {url}")
            else:
                print(f"Error adding attribute to MISP: {response.status_code}, {response.text}")
        
        except requests.exceptions.RequestException as e:
            print(f"MISP API request error: {e}")

def publish_event():
    try:
        response = requests.post(publish_url, headers=misp_headers, verify=False)
        
        if response.status_code == 200:
            print(f"Event ID {misp_event_id} successfully published.")
        else:
            print(f"Error publishing event: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"MISP API request error while publishing event: {e}")

