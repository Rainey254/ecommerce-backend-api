from flask import Blueprint, request, jsonify
from utils.db import audit_logs_collection
from models.audit_log import AuditLog
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth import check_role

audit_logs_bp = Blueprint('audit_logs', __name__)
audit_log_model = AuditLog(audit_logs_collection)

# Log an action
@audit_logs_bp.route('/audit-logs', methods=['POST'])
@jwt_required()
def log_action():
    data = request.get_json()
    required_fields = ['action', 'user_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400

    audit_log_model.log_action(data)
    return jsonify({'message': 'Action logged successfully'}), 201

# Get all logs (Admin only)
@audit_logs_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_all_logs():
    user = get_jwt_identity()
    if not check_role(user, 'admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    logs = audit_log_model.find_all_logs()
    for log in logs:
        log['_id'] = str(log['_id'])
    return jsonify(logs), 200