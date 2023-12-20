from flask import url_for
from app.domain.Task import Status


def test_get_all_tasks(test_client, db, login_default_user):
    response = test_client.get(url_for('task.tasks'))
    assert response.status_code == 200
    assert [task_name in response.text for task_name in ['Task1', 'Task2', 'Task3', 'Task4']]


def test_add_correct_task(test_client, db, login_default_user):
    data = {
        'name': 'Task6',
        'description': 'Description'
    }
    response = test_client.post(url_for('task.add_task'), data=data, follow_redirects=True)
    assert response.status_code == 200
    assert data['name'] in response.text


def test_add_incorrect_task(test_client, db, login_default_user):
    data = {
        'name': 'Task1',
        'description': 'My task description',
        'status': Status.TODO.name
    }
    response = test_client.post(url_for('task.add_task', id=1), data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "There is the Task with this name." in response.text


def test_edit_task(test_client, db, login_default_user):
    data = {
        'name': 'Task1',
        'description': 'My task description',
        'status': Status.TODO.name
    }
    response = test_client.post(url_for('task.update_task', id=1), data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "You have successfully updated task" in response.text


def test_task_delete(test_client, db, login_default_user):
    response = test_client.get(url_for('task.delete_task', id=1), follow_redirects=True)
    assert response.status_code == 200
    assert "You have successfully deleted task" in response.text
