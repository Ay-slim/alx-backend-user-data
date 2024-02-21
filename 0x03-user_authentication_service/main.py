#!/usr/bin/env python3


"""Test functions and endpoints end to end"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Function to test the register user endpont
    """
    result = requests.post(
            'http://localhost:5000/users',
            data={'email': email, 'password': password})
    res_data = result.json()

    assert len(res_data.keys()) == 2
    assert result.status_code == 200
    assert type(res_data) is dict
    assert 'message' in res_data
    assert 'email' in res_data
    assert res_data['message'] == 'user created'
    assert res_data['email'] == email

    result = requests.post(
            'http://localhost:5000/users',
            data={'email': email, 'password': password})
    res_data = result.json()

    assert result.status_code == 400
    assert 'email' not in res_data
    assert 'message' in res_data
    assert type(res_data) is dict
    assert len(res_data.keys()) == 1
    assert res_data['message'] == 'email already registered'


def log_in_wrong_password(email: str, password: str) -> None:
    """Assert that a response error is thrown for wrong password login"""
    result = requests.post(
            'http://localhost:5000/sessions',
            data={'email': email, 'password': password})

    assert result.status_code == 401


def log_in(email: str, password: str) -> str:
    """Validates that the login endpoint returns appropriately"""
    result = requests.post(
            'http://localhost:5000/sessions',
            data={'email': email, 'password': password})
    cookies = result.cookies
    res_data = result.json()

    assert result.status_code == 200
    assert 'email' in res_data
    assert 'message' in res_data
    assert res_data['email'] == email
    assert res_data['message'] == 'logged in'
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'session_id' in cookies

    return cookies.get('session_id')


def profile_unlogged() -> None:
    """Validates that an error response is thrown when not logged in"""
    result = requests.get('http://localhost:5000/profile')

    assert result.status_code == 403


def profile_logged(session_id: str) -> None:
    """Validate profile return for a logged in user"""
    result = requests.get(
            'http://localhost:5000/profile',
            cookies={'session_id': session_id})
    res_data = result.json()

    assert result.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 1
    assert 'email' in res_data


def log_out(session_id: str) -> None:
    """Tests the logout endpoint"""
    result = requests.delete(
            'http://localhost:5000/sessions',
            cookies={'session_id': session_id})

    assert result.status_code == 200


def reset_password_token(email: str) -> str:
    """Tests password reset token generation"""
    result = requests.post(
            'http://localhost:5000/reset_password',
            data={'email': email})
    res_data = result.json()

    assert result.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'reset_token' in res_data
    assert res_data['email'] == email

    return res_data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests the password update endpoint"""
    result = requests.put(
            'http://localhost:5000/reset_password',
            data={
                'email': email,
                'reset_token': reset_token,
                'new_password': new_password})
    res_data = result.json()

    assert result.status_code == 200
    assert type(res_data) is dict
    assert len(res_data.keys()) == 2
    assert 'email' in res_data
    assert 'message' in res_data
    assert res_data['email'] == email
    assert res_data['message'] == 'Password updated'


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
