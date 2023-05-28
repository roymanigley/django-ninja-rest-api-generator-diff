from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from dummy_app.rest.auth import verify_token, is_token_expired
from dummy_app.tests_rest.helper import create_inactive_user, create_active_user

VALID_PASSWORD = 'password'
VALID_USERNAME = 'username'

INVALID_PASSWORD = 'wrong_password'
INVALID_USERNAME = 'wrong_username'


class LoginTest(TestCase):
    def setUp(self):
        create_active_user(VALID_USERNAME, VALID_PASSWORD)
        self.client = Client()

    def test_login_success(self):
        # WHEN
        response = self.client.post(f'/api/login?username={VALID_USERNAME}&password={VALID_PASSWORD}')

        # THEN
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        self.assertTrue(
            verify_token(token)
        )
        self.assertFalse(
            is_token_expired(token)
        )

    def test_inactive_user_with_correct_credentials(self):
        inactive_user_username = 'some_inactive_user'
        inactive_user_password = '1234'
        create_inactive_user(inactive_user_username, inactive_user_password)
        # WHEN
        response = self.client.post(f'/api/login?username={inactive_user_username}&password={inactive_user_password}')

        # THEN
        self.assertEqual(response.status_code, 401)
        no_token = 'token' not in response.json().keys()
        error_text = response.json()["error"]
        self.assertTrue(
            no_token
        )
        self.assertEqual(error_text, 'access denied')

    def test_login_fail_invalid_username_and_password(self):
        # WHEN
        response = self.client.post(f'/api/login?username={INVALID_PASSWORD}&password={INVALID_USERNAME}')

        # THEN
        self.assertEqual(response.status_code, 401)
        no_token = 'token' not in response.json().keys()
        error_text = response.json()["error"]
        self.assertTrue(
            no_token
        )
        self.assertEqual(error_text, 'access denied')

    def test_login_fail_invalid_password(self):
        # WHEN
        response = self.client.post(f'/api/login?username={VALID_USERNAME}&password={INVALID_PASSWORD}')

        # THEN
        self.assertEqual(response.status_code, 401)
        no_token = 'token' not in response.json().keys()
        error_text = response.json()["error"]
        self.assertTrue(
            no_token
        )
        self.assertEqual(error_text, 'access denied')

    def test_login_fail_invalid_username(self):
        # WHEN
        response = self.client.post(f'/api/login?username={INVALID_USERNAME}&password={VALID_PASSWORD}')

        # THEN
        self.assertEqual(response.status_code, 401)
        no_token = 'token' not in response.json().keys()
        error_text = response.json()["error"]
        self.assertTrue(
            no_token
        )
        self.assertEqual(error_text, 'access denied')

    def test_login_fail_valid_username_and_password_switched(self):
        # WHEN
        response = self.client.post(f'/api/login?username={VALID_PASSWORD}&password={VALID_USERNAME}')

        # THEN
        self.assertEqual(response.status_code, 401)
        no_token = 'token' not in response.json().keys()
        error_text = response.json()["error"]
        self.assertTrue(
            no_token
        )
        self.assertEqual(error_text, 'access denied')
