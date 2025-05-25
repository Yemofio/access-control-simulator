import jwt
import time
from functools import wraps
from flask import request, jsonify
from jwt.exceptions import InvalidTokenError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from typing import List, Dict

class AuthService:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def generate_token(self, user_id: str, roles: List[str]) -> str:
        """Generate JWT token with user claims"""
        payload = {
            'sub': user_id,
            'roles': roles,
            'iat': int(time.time()),
            'exp': int(time.time()) + 3600  # 1 hour expiration
        }
        return jwt.encode(
            payload,
            self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ),
            algorithm='RS256'
        )
    
    def verify_token(self, token: str) -> Dict:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ),
                algorithms=['RS256']
            )
            return payload
        except InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")

def requires_auth(roles: List[str] = None):
    """Decorator for endpoints requiring authentication"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"error": "Authorization header missing"}), 401
            
            try:
                token = auth_header.split()[1]
                auth = AuthService()
                payload = auth.verify_token(token)
                
                if roles and not any(role in payload['roles'] for role in roles):
                    return jsonify({"error": "Insufficient permissions"}), 403
                
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({"error": str(e)}), 401
        return wrapped
    return decorator