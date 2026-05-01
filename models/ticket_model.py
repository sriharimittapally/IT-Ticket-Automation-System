from database.db import get_db_connection

def save_ticket(issue, sn_id, jira_id, azure_id):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tickets (issue, status, servicenow_id, jira_id, azure_id) VALUES (?, ?, ?, ?, ?)",
        (issue, "Open", sn_id, jira_id, azure_id)
    )
    conn.commit()
    conn.close()


def update_ticket_status(ticket_id, status):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (status, ticket_id)
    )
    conn.commit()
    conn.close()


def get_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    return ticket