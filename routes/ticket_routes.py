from flask import Blueprint, request, jsonify
from models.ticket_model import save_ticket, update_ticket_status, get_ticket
from services.servicenow_service import create_servicenow_ticket, update_servicenow_ticket
from services.jira_service import create_jira_ticket, update_jira_ticket
from services.azure_service import create_azure_work_item, update_azure_work_item

ticket_bp = Blueprint('ticket_bp', __name__)


@ticket_bp.route('/create_ticket', methods=['POST'])
def create_ticket():
    data = request.json
    if not data or 'issue' not in data:
        return jsonify({"error": "Issue is required"}), 400

    issue = data['issue']

    # ServiceNow
    sn_status, sn_id = create_servicenow_ticket(issue)

    # Jira
    jira_id = None
    if "bug" in issue.lower() or "error" in issue.lower():
        _, jira_id = create_jira_ticket(issue, issue)

    # Azure (ALWAYS create)
    _, azure_id = create_azure_work_item(issue, issue)

    # Save all
    save_ticket(issue, sn_id, jira_id, azure_id)

    return jsonify({
        "message": "Ticket created",
        "servicenow_id": sn_id,
        "jira_id": jira_id,
        "azure_id": azure_id
    })
    data = request.json

    if not data or 'issue' not in data:
        return jsonify({"error": "Issue is required"}), 400

    issue = data['issue']   # ✅ THIS WAS MISSING

    # Create ServiceNow ticket
    sn_status, sn_id = create_servicenow_ticket(issue)

    jira_status = None
    jira_id = None

    # Create Jira ticket only for bugs
    if "bug" in issue.lower() or "error" in issue.lower():
        jira_status, jira_id = create_jira_ticket(issue, issue)

    # Save in DB
    save_ticket(issue, sn_id, jira_id)

    return jsonify({
        "message": "Ticket created",
        "servicenow_id": sn_id,
        "jira_id": jira_id
    })

@ticket_bp.route('/update_status/<int:ticket_id>', methods=['PUT'])
def update_status(ticket_id):
    data = request.json
    status = data.get('status')

    if not status:
        return jsonify({"error": "Status required"}), 400

    update_ticket_status(ticket_id, status)

    ticket = get_ticket(ticket_id)

    sn_status = None
    jira_status = None
    azure_status = None

    # Index mapping:
    # ticket[3] = servicenow_id
    # ticket[4] = jira_id
    # ticket[5] = azure_id

    if ticket[3]:
        sn_status = update_servicenow_ticket(ticket[3], status)

    if ticket[4]:
        jira_status = update_jira_ticket(ticket[4], status)

    if ticket[5]:
        azure_status = update_azure_work_item(ticket[5], status)

    return jsonify({
        "message": "Status updated",
        "servicenow_update": sn_status,
        "jira_update": jira_status,
        "azure_update": azure_status
    })
    data = request.json
    status = data.get('status')

    update_ticket_status(ticket_id, status)

    ticket = get_ticket(ticket_id)

    sn_status = None
    jira_status = None

    if ticket[3]:
        sn_status = update_servicenow_ticket(ticket[3], status)

    if ticket[4]:
        jira_status = update_jira_ticket(ticket[4], status)

    return jsonify({
        "message": "Status updated",
        "servicenow_update": sn_status,
        "jira_update": jira_status
    })