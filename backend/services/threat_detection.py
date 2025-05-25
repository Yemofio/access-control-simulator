from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict

class ThreatDetector:
    def __init__(self):
        self.access_patterns = defaultdict(list)
        self.thresholds = {
            'failed_attempts': 5,
            'time_window': timedelta(minutes=15),
            'unusual_hour': 3  # 3 AM
        }
    
    def analyze_access(self, user_id: str, resource_id: str, timestamp: datetime) -> Dict:
        """Analyze access patterns for potential threats"""
        self.access_patterns[user_id].append((resource_id, timestamp))
        
        # Check for brute force attempts
        recent_attempts = [
            t for r, t in self.access_patterns[user_id] 
            if t > datetime.now() - self.thresholds['time_window']
        ]
        
        alerts = []
        
        if len(recent_attempts) > self.thresholds['failed_attempts']:
            alerts.append({
                'type': 'BRUTE_FORCE',
                'severity': 'HIGH',
                'message': f'Multiple failed access attempts by {user_id}'
            })
        
        # Check for unusual access time
        if timestamp.hour <= self.thresholds['unusual_hour']:
            alerts.append({
                'type': 'UNUSUAL_TIME',
                'severity': 'MEDIUM',
                'message': f'User {user_id} accessing system at unusual hour'
            })
        
        # Check for privilege escalation patterns
        sensitive_resources = ['admin_console', 'user_db', 'billing']
        if resource_id in sensitive_resources:
            alerts.append({
                'type': 'SENSITIVE_ACCESS',
                'severity': 'LOW',
                'message': f'User {user_id} accessing sensitive resource {resource_id}'
            })
        
        return {
            'user_id': user_id,
            'resource_id': resource_id,
            'timestamp': timestamp.isoformat(),
            'alerts': alerts
        }