import unittest

from flask import url_for

from test.base_test import BaseTest


class GeneralPagesTest(BaseTest):

    def test_home_page_test(self):
        """
         Test for home page.
         Checks if endpoint returns a page with correct content
        """
        with self.client:
            response = self.client.get(url_for('general.home'))
            self.assert200(response)
            self.assertIn(b'Lorem ipsum', response.data)

    def test_about_page_test(self):
        """
         Test for about page.
         Checks if endpoint returns a page with correct content
        """
        with self.client:
            response = self.client.get(url_for('general.about'))
            self.assert200(response)
            self.assertIn(b'Hello, my name is Arsen', response.data)

    def test_contacts_page(self):
        """
         Test for contacts page.
         Checks if endpoint returns a page with correct content
        """
        with self.client:
            response = self.client.get(url_for('general.contacts'))
            self.assert200(response)
            self.assertIn(b'GitHub', response.data)

    def test_skills_page(self):
        """
         Test for skills page.
         Checks if endpoint returns a page with correct content
         Also it checks if the endpoint receives correct skill id and show it
        """
        with self.client:
            response = self.client.get(url_for('general.skills'))
            self.assert200(response)
            self.assertIn(b'Java', response.data)
            self.assertIn(b'PHP', response.data)
            self.assertIn(b'C++', response.data)

            response = self.client.get(url_for('general.skills', id='Java'))
            self.assert200(response)
            self.assertIn(b'Java', response.data)

            response = self.client.get(url_for('general.skills', id='Jawa'))
            self.assert200(response)
            self.assertIn(b'Undefined!', response.data)


if __name__ == 'main':
    unittest.main()
