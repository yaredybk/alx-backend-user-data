#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from db import DB
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
from flask.helpers import make_response
from auth import Auth
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ Base route for authentication service API """
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """Registers a new user if it does not exist before"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """log in"""
    user_request = request.form
    user_email = user_request.get('email', '')
    user_password = user_request.get('password', '')
    valid_log = AUTH.valid_login(user_email, user_password)
    if not valid_log:
        abort(401)
    response = make_response(jsonify({"email": user_email,
                                      "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
