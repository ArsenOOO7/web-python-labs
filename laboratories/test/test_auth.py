import unittest

from flask import url_for
from flask_login import current_user

from app.domain.User import User
from test.base_test import BaseTest


class AuthTest(BaseTest):

    def test_register_success(self):
        """
        Register page test.
        Checks if the user is correctly saved to the database.
        """

        with self.client:
            register_user_data = {
                'username': 'user3',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'email': 'user3@mail.com',
                'password': 'mySecretPassword123',
                'confirm_password': 'mySecretPassword123',
                'birth_date': '2023-11-01'
            }
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn('You successfully created an account', response.text)

            expected_id = 3
            registered_user = User.query.get(expected_id)
            self.assertIsNotNone(registered_user)
            self.assertEqual(register_user_data['username'], registered_user.username)

    def test_register_on_exists_creds(self):
        """
        Assume that user cannot sign up with already existing emails and usernames
        """
        with self.client:
            register_user_data = {
                'username': 'user3',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'email': 'user1@mail.com',
                'password': 'mySecretPassword123',
                'confirm_password': 'mySecretPassword123',
                'birth_date': '2023-11-01'
            }
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Email already exists.', response.data)

            register_user_data['email'] = 'user3@mail.com'
            register_user_data['username'] = 'user1'
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Username already exists.', response.data)

    def test_login_success(self):
        """
        Checks if user can sign in with valid credentials
        """
        with self.client:
            login_user_data = {
                'login': 'user1',
                'password': '1234',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'You successfully logged in.', response.data)

    def test_login_with_incorrect_data(self):
        """
        Checks if user can sign in with valid credentials
        """
        with self.client:
            login_user_data = {
                'login': 'user1',
                'password': '12345',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Invalid credentials.', response.data)

    def test_logout(self):
        """
        Checks if user can log out
        """
        with self.client:
            login_user_data = {
                'login': 'user1',
                'password': '1234',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'You successfully logged in.', response.data)

            self.assertTrue(current_user.is_authenticated)
            response = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'You have successfully logged out!', response.data)


if __name__ == 'main':
    unittest.main()
