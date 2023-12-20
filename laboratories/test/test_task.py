from flask import url_for
from flask_login import login_user

from app.domain.Task import Status
from app.domain.User import User
from test.base_test import BaseTest


class TaskTest(BaseTest):

    def setUp(self):
        super().setUp()
        login_user(User.query.get(1))

    def test_get_all_tasks(self):
        """
        This test checks if tasks are correctly displayed on page
        """
        with self.client:
            response = self.client.get(url_for('task.tasks'))
            self.assert200(response)
            [self.assertIn(task_name, response.text) for task_name in ['Task1', 'Task2', 'Task3', 'Task4']]

    def test_task_correct_add(self):
        """
        Assures that new task will be added correctly
        """
        with self.client:
            task_data = {
                'name': 'Task6',
                'description': 'My task description'
            }
            response = self.client.post(url_for('task.add_task'), data=task_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(task_data['name'], response.text)

    def test_task_incorrect_add(self):
        """
        Checks if error will be displayed when trying to insert task with existing name
        """
        with self.client:
            task_data = {
                'name': 'Task1',
                'description': 'My task description',
                'status': Status.TODO
            }
            response = self.client.post(url_for('task.add_task', id=1), data=task_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("There is the Task with this name.", response.text)

    def test_task_edit(self):
        """
        The same as add new one, but it's about updating existing one
        """
        with self.client:
            task_data = {
                'name': 'Task1',
                'description': 'My task description',
                'status': Status.TODO.name
            }
            response = self.client.post(url_for('task.update_task', id=1), data=task_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("You have successfully updated task", response.text)

    def test_task_delete(self):
        """
        Checking task deletion
        """
        with self.client:
            response = self.client.get(url_for('task.delete_task', id=1), follow_redirects=True)
            self.assert200(response)
            self.assertIn("You have successfully deleted task", response.text)
