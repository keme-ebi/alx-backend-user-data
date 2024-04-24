#!/usr/bin/env python3
"""basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def basic():
    """returns a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """registers a user"""
    email, password = request.form.get('email'), request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """user login"""
    email, password = request.form.get('email'), request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """user logout"""
    resp = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(resp)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', strict_slashes=False)
def profile():
    """user profile"""
    resp = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(resp)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """reset password token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """updates the user password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
