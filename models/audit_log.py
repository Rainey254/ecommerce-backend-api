from pymongo.collection import Collection
from datetime import datetime

class AuditLog:
    def __init__(self, collection: Collection):
        self.collection = collection

    def log_action(self, log_data):
        """Insert a new log entry."""
        log_data['timestamp'] = datetime.now()
        return self.collection.insert_one(log_data)

    def find_all_logs(self):
        """Retrieve all log entries."""
        return list(self.collection.find())