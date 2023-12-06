import unittest

from flask import url_for
from flask_login import current_user

from test.base_test import BaseTest


class UserTest(BaseTest):

    def test_change_user_data_without_email_and_username(self):
        """
        This test checks if user can change their data
        Like logout, we should sign in with our user, then send next request to change theirs data
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

            change_data = {
                'first_name': 'Firstnameuserone',
                'last_name': 'Lastnameuserone',
                'about_me': 'Another string about me.',
                'birth_date': '2023-11-01',
                'email': 'user1@mail.com',
                'username': 'user1'
            }

            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'You successfully updated your account details!', response.data)
            self.assertIn(change_data['first_name'], response.text)
            self.assertIn(change_data['last_name'], response.text)
            self.assertIn(change_data['about_me'], response.text)

    def test_change_user_data_with_email_and_username(self):
        """
        This test checks if user can change their data
        But now he will change his email and username
        Like logout, we should sign in with our user, then send next request to change theirs data
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

            change_data = {
                'first_name': 'Firstnameuserone',
                'last_name': 'Lastnameuserone',
                'about_me': 'Another string about me.',
                'birth_date': '2023-11-01',
                'email': 'user2@mail.com',
                'username': 'user1'
            }

            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("Email already exists.", response.text)

            change_data['email'] = 'user1@mail.com'
            change_data['username'] = 'user2'
            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("Username already exists.", response.text)


if __name__ == 'main':
    unittest.main()
