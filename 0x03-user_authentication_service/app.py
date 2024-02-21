#!/usr/bin/env python3
"""User session flask app module"""
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    request,
    redirect,
    url_for,
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Base api route"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register a new user endpoint"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
       Endpoint to log user in by creating a session
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify(
        {"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """User logout function"""
    session_id = request.cookies.get('session_id')

    try:
        user = AUTH.get_user_from_session_id(session_id)
    except Exception:
        abort(403)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Fetches a user's profile using their session id"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Endpoint for generating a password reset token"""

    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Endpoint to change password and invalidate reset token"""
    email = request.form.get('email')
    password = request.form.get('password')
    reset_token = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, password)
        return jsonify({'email': email, 'message': 'Password updated'})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
