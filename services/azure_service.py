import requests
from requests.auth import HTTPBasicAuth
from config.settings import AZURE_ORG_URL, AZURE_PROJECT, AZURE_PAT


def create_azure_work_item(title, description):
    url = f"{AZURE_ORG_URL}/{AZURE_PROJECT}/_apis/wit/workitems/$Task?api-version=7.0"

    headers = {
        "Content-Type": "application/json-patch+json"
    }

    payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": description
        }
    ]

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth("", AZURE_PAT)
    )

    print("Azure Status:", response.status_code)
    print("Azure Response:", response.text)

    if response.status_code in [200, 201]:
        return response.status_code, response.json()['id']

    return response.status_code, None



def update_azure_work_item(work_item_id, status):
    url = f"{AZURE_ORG_URL}/{AZURE_PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0"

    state_map = {
        "Open": "New",
        "In Progress": "Active",
        "Resolved": "Closed"
    }

    payload = [
        {
            "op": "add",
            "path": "/fields/System.State",
            "value": state_map.get(status, "New")
        }
    ]

    response = requests.patch(
        url,
        headers={"Content-Type": "application/json-patch+json"},
        json=payload,
        auth=HTTPBasicAuth("", AZURE_PAT)
    )

    return response.status_code