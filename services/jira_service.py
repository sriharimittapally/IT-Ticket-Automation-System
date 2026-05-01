import requests
from requests.auth import HTTPBasicAuth
from config.settings import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY


def create_jira_ticket(summary, description):
    url = f"{JIRA_URL}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{
                        "type": "text",
                        "text": description
                    }]
                }]
            },
            "issuetype": {"name": "Task"}
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    if response.status_code in [200, 201]:
        return response.status_code, response.json()['key']
    return response.status_code, None


def update_jira_ticket(issue_key, status):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions"

    transition_map = {
        "In Progress": "21",
        "Resolved": "31"
    }

    transition_id = transition_map.get(status)

    if not transition_id:
        print("No valid transition for status:", status)
        return None

    payload = {
        "transition": {"id": transition_id}
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    print("Jira Update Status:", response.status_code)
    print("Jira Update Response:", response.text)

    return response.status_code