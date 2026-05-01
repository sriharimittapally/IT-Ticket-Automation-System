from flask import Blueprint, request, jsonify
from models.ticket_model import save_ticket, update_ticket_status, get_ticket
from services.servicenow_service import create_servicenow_ticket, update_servicenow_ticket
from services.jira_service import create_jira_ticket, update_jira_ticket
from services.azure_service import create_azure_work_item, update_azure_work_item

ticket_bp = Blueprint('ticket_bp', __name__)


# ---------------- CREATE TICKET ----------------
@ticket_bp.route('/create_ticket', methods=['POST'])
def create_ticket():
    data = request.json

    if not data or 'issue' not in data:
        return jsonify({"error": "Issue is required"}), 400

    issue = data['issue']

    # ServiceNow
    _, sn_id = create_servicenow_ticket(issue)

    # Jira (only for bugs)
    jira_id = None
    if "bug" in issue.lower() or "error" in issue.lower():
        _, jira_id = create_jira_ticket(issue, issue)

    # Azure (always)
    _, azure_id = create_azure_work_item(issue, issue)

    # Save in DB
    save_ticket(issue, sn_id, jira_id, azure_id)

    return jsonify({
        "message": "Ticket created",
        "servicenow_id": sn_id,
        "jira_id": jira_id,
        "azure_id": azure_id
    })


# ---------------- UPDATE STATUS ----------------
@ticket_bp.route('/update_status/<int:ticket_id>', methods=['PUT'])
def update_status(ticket_id):
    data = request.json
    status = data.get('status')

    if not status:
        return jsonify({"error": "Status required"}), 400

    update_ticket_status(ticket_id, status)

    ticket = get_ticket(ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    sn_status = None
    jira_status = None
    azure_status = None

    if ticket['servicenow_id']:
        sn_status = update_servicenow_ticket(ticket['servicenow_id'], status)

    if ticket['jira_id']:
        jira_status = update_jira_ticket(ticket['jira_id'], status)

    if ticket['azure_id']:
        azure_status = update_azure_work_item(ticket['azure_id'], status)

    return jsonify({
        "message": "Status updated",
        "servicenow_update": sn_status,
        "jira_update": jira_status,
        "azure_update": azure_status
    })