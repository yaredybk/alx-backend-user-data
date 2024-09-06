#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': user_email})
    if users is None:
        return jsonify({"error": "no user found for this email"}), 404
    user = None
    password = User.is_valid_password(password)
    for u in users:
        if u.password == password:
            user = u
            break
    if user is None:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv("SESSION_NAME"), session_id)
    return res
