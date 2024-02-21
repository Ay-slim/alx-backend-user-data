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
    """ the base index route for api """
    return jsonify({'message': 'Bienvenue'})
