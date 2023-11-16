from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()

BLOCKLIST = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
