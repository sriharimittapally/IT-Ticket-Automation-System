# IT Support Ticket Automation System

## 📌 Overview

The IT Support Ticket Automation System is a backend-based application designed to automate the handling of IT support issues.
It integrates multiple industry tools to streamline ticket creation, tracking, and resolution.

The system eliminates manual coordination between IT support teams and developers by automatically creating and updating tickets across platforms.

---

## 🎯 Objectives

* Accept user-reported issues
* Automatically create tickets
* Track development work
* Synchronize ticket status across systems
* Improve coordination between IT support and development teams

---

## 🏗️ System Architecture

```
User → Flask API
       ├── SQLite Database (local storage)
       ├── ServiceNow (Incident Management)
       ├── Jira (Bug Tracking)
       └── Azure Boards (Work Tracking)
```

---

## 🔄 Workflow

1. User submits an issue
2. Flask backend receives the request
3. Ticket is stored in local database
4. ServiceNow incident is created
5. If issue contains "bug" or "error":

   * Jira task is created
6. Azure Board work item is created
7. When status is updated:

   * ServiceNow → updated
   * Jira → moved to next state
   * Azure → state updated

---

## ⚙️ Technologies Used

* Python (Flask)
* SQLite (Database)
* REST APIs
* ServiceNow API
* Jira API (Atlassian)
* Azure DevOps Boards

---

## 📁 Project Structure

```
IT_TICKET_SYSTEM/
│
├── config/
│   └── settings.py
│
├── database/
│   └── db.py
│
├── models/
│   └── ticket_model.py
│
├── routes/
│   └── ticket_routes.py
│
├── services/
│   ├── servicenow_service.py
│   ├── jira_service.py
│   └── azure_service.py
│
├── app.py
├── database.db
├── .env (NOT INCLUDED)
├── requirements.txt
└── README.md
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory and add:

```
JIRA_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
JIRA_PROJECT_KEY=

SERVICENOW_URL=
SERVICENOW_USER=
SERVICENOW_PASSWORD=

AZURE_ORG_URL=
AZURE_PROJECT=
AZURE_PAT=
```

⚠️ Note:
Do NOT share or upload `.env` file (contains sensitive credentials)

---

## 🚀 Installation & Running

1. Clone or download the project

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Configure `.env` file (as above)

4. Run the application:

```
python app.py
```

5. Server runs at:

```
http://127.0.0.1:5000
```

---

## 📬 API Endpoints

### 1️⃣ Create Ticket

**POST** `/create_ticket`

Request Body:

```
{
  "issue": "Login bug issue"
}
```

Response:

```
{
  "message": "Ticket created",
  "servicenow_id": "...",
  "jira_id": "...",
  "azure_id": "..."
}
```

---

### 2️⃣ Update Ticket Status

**PUT** `/update_status/<ticket_id>`

Request Body:

```
{
  "status": "Resolved"
}
```

Valid Status:

* Open
* In Progress
* Resolved

Response:

```
{
  "message": "Status updated",
  "servicenow_update": 200,
  "jira_update": 204,
  "azure_update": 200
}
```

---

## 🧠 Key Features

* Multi-system integration (ServiceNow, Jira, Azure)
* Conditional Jira ticket creation (only for bugs)
* Centralized status synchronization
* Local database tracking
* REST API-based architecture

---

## ⚠️ Error Handling

* Basic validation for input
* API response status tracking
* Partial success handling (if one service fails)

---

## 🔍 Assumptions

* Jira workflow supports transitions (To Do → In Progress → Done)
* ServiceNow credentials have API access
* Azure DevOps project and PAT token are configured

---

## 🚧 Limitations

* No frontend UI (API-based interaction)
* Minimal error logging
* No authentication layer
* SQLite used (not production DB)

---

## 📈 Future Improvements

* Add frontend interface
* Implement authentication & authorization
* Add logging system
* Deploy on cloud
* Replace SQLite with PostgreSQL
* Add notifications (email/Slack)

---

## 💡 Conclusion

This project demonstrates how multiple enterprise tools can be integrated into a unified IT support workflow system.
It improves efficiency, tracking, and coordination between teams using automation.

---
