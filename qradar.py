import requests
import json
import time
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

qradar_token = "<YOUR_QRADAR_API_TOKEN>"
qradar_api_url = "https://<YOUR_QRADAR_URL>/api/siem/offenses"
qradar_headers = {
    'SEC': f'{qradar_token}'
}

def get_offenses():
    # replace the @ characters below with the "rule ids" of your qradar web rules (for example: 101345 and etc.)
    offenses_url = f"{qradar_api_url}?filter=status%3DOPEN%20and%20rules%20contains%20(id%3D@%20OR%20id%3D@%20OR%20id%3D@%20OR%20id%3D@)" # of course, you can add more id with OR operators
    # you can find qradar api filters documentation in here - https://www.ibm.com/docs/en/qradar-common?topic=versions-filter-syntax
    response = requests.get(offenses_url, headers=qradar_headers, verify=False)
    
    if response.status_code == 200:
        try:
            offenses = response.json()
            print(f"Found {len(offenses)} open offense(s)")
            return offenses
        except json.JSONDecodeError:
            print("An error occurred in the JSON format. Response:", response.text)
            return []
    else:
        print(f"Error fetching offenses: {response.status_code}, {response.text}")
        return []

def get_source_ip_and_url(offenses):
    ip_and_urls = []
    
    for offense in offenses:
        offense_id = offense['id']
        source_ip = offense['offense_source']

        print(f"\n--- Process starting: Offense ID: {offense_id}, Source IP: {source_ip} ---\n")

        aql_query = 'SELECT "URL Query String" FROM events WHERE sourceip=\'{}\' AND "URL Query String" IS NOT NULL AND "URL Query String" != \'/\' LIMIT 1 LAST 1 DAYS'.format(source_ip)
        aql_url = "https://<YOUR_QRADAR_URL>/api/ariel/searches" 
        
        payload = {
            "query_expression": aql_query
        }
        
        try:
            response = requests.post(aql_url, headers=qradar_headers, data=payload, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            continue
        
        if response.status_code == 201:
            search_id = response.json().get("search_id")
            search_results_url = f"https://<YOUR_QRADAR_URL>/api/ariel/searches/{search_id}/results"
            
            time.sleep(0.8)
            
            try:
                results_response = requests.get(search_results_url, headers=qradar_headers, verify=False)
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                continue
            
            if results_response.status_code == 200:
                try:
                    search_results = results_response.json()
                    if 'events' in search_results and len(search_results['events']) > 0:
                        url = search_results['events'][0].get('URL Query String')
                        ip_and_urls.append((source_ip, url))
                    else:
                        print(f"URL not found for this IP: {source_ip}")
                except json.JSONDecodeError:
                    print("An error occurred in the JSON format. Response:", results_response.text)
            else:
                print(f"Search results not retrieved, search_id {search_id}, Error code: {results_response.status_code}")
    return ip_and_urls
