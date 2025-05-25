import numpy as np
from datetime import datetime
from typing import Dict, List,Tuple
from enum import Enum, auto
from functools import reduce

class ZeroTrustEngine:
    def __init__(self):
        self.risk_factors = {
            'location': {
                'office': 0.1,
                'remote': 0.3,
                'foreign': 0.7
            },
            'time': {
                'business_hours': 0.1,
                'after_hours': 0.4
            },
            'device': {
                'managed': 0.1,
                'unmanaged': 0.6
            }
        }
    
    def calculate_risk_score(self, context: Dict) -> float:
        """Calculate dynamic risk score based on context"""
        base_score = 0.5  # Default medium risk
        
        # Location risk
        location = context.get('location', 'remote')
        base_score += self.risk_factors['location'].get(location, 0.3)
        
        # Time risk
        hour = datetime.now().hour
        time_key = 'business_hours' if 9 <= hour <= 17 else 'after_hours'
        base_score += self.risk_factors['time'][time_key]
        
        # Device risk
        device = context.get('device', 'unmanaged')
        base_score += self.risk_factors['device'].get(device, 0.5)
        
        # Apply sigmoid function to normalize between 0-1
        risk_score = 1 / (1 + np.exp(-(base_score - 0.5) * 10))
        return round(risk_score, 2)
    
    def determine_authentication_level(self, risk_score: float) -> int:
        """Determine required auth level based on risk"""
        if risk_score < 0.3:
            return 1  # Single-factor
        elif risk_score < 0.7:
            return 2  # Multi-factor
        else:
            return 3  # Step-up & biometrics
        
        return 0
    
class PolicyEffect(Enum):
    ALLOW = auto()
    DENY = auto()
    INDETERMINATE = auto()

class PolicyCombiningAlgorithm:
    @staticmethod
    def deny_overrides(policies: List[Tuple[PolicyEffect, str]]) -> Tuple[PolicyEffect, List[str]]:

        reasons = []
        for effect, reason in policies:
            reasons.append(reason)
            if effect == PolicyEffect.ALLOW:
                return (PolicyEffect.ALLOW, reasons)
        return (PolicyEffect.DENY, reasons)
    
    @staticmethod
    def first_applicable(policies: List[Tuple[PolicyEffect, str]]) -> Tuple[PolicyEffect, List[str]]:
        return policies[0] if policies else (PolicyEffect.INDETERMINATE, ["No policies applied"])

class AdvancedPolicyEngine:
    def __init__(self):
        self.algorithm = PolicyCombiningAlgorithm.deny_overrides
    
    def evaluate(self, request: Dict, policies: List[Dict]) -> Tuple[PolicyEffect, List[str]]:
        """Evaluate request against all policies with conflict resolution"""
        evaluated_policies = []
        
        for policy in policies:
            effect, reason = self._evaluate_single_policy(request, policy)
            evaluated_policies.append((effect, reason))
        
        return self.algorithm(evaluated_policies)
    
    def _evaluate_single_policy(self, request: Dict, policy: Dict) -> Tuple[PolicyEffect, str]:
        """Evaluate a single policy against the request"""
        # Implementation of policy evaluation
        # This would check conditions, rules, etc.
        return (PolicyEffect.ALLOW, "Policy satisfied")