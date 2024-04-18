#!/usr/bin/env python3
"""routes for the Session authentication"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def auth_session_login() -> str:
    """handles user login"""
    email, password = request.form.get('email'), request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session = auth.create_session(user.id)
            user_rep = jsonify(user.to_json())
            ses_name = os.getenv('SESSION_NAME')
            user_rep.set_cookie(ses_name, session)
            return user_rep

@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """handles user logout"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)
    return jsonify({}), 200
