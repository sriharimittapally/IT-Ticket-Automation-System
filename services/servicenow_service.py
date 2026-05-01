import requests
from config.settings import SERVICENOW_URL, SERVICENOW_USER, SERVICENOW_PASSWORD

BASE_URL = SERVICENOW_URL

def create_servicenow_ticket(issue):
    url = f"{BASE_URL}/api/now/table/incident"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "short_description": issue,
        "description": issue,
        "caller_id": SERVICENOW_USER
    }

    response = requests.post(
        url,
        auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
        headers=headers,
        json=data
    )

    if response.status_code in [200, 201]:
        return response.status_code, response.json()['result']['sys_id']
    return response.status_code, None


def update_servicenow_ticket(sys_id, status):
    url = f"{BASE_URL}/api/now/table/incident/{sys_id}"

    state_map = {
        "Open": "1",
        "In Progress": "2",
        "Resolved": "6"
    }

    data = {"state": state_map.get(status, "1")}

    response = requests.put(
        url,
         auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
        headers={"Content-Type": "application/json"},
        json=data
    )

    return response.status_code