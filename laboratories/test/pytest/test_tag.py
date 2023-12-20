from flask import url_for


def test_add_tag(test_client, db, login_default_user):
    data = {
        'name': 'Test Tag #10',
        'color': 'INFO'
    }
    response = test_client.post(url_for('post.tag.create_tag_handle'), data=data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Test Tag #10' in response.text


def test_tag_list(test_client, db, login_default_user):
    response = test_client.get(url_for('post.tag.tag_list'))
    assert [tag_name in response.text for tag_name in ['Test Tag #1', 'Test Tag #2', 'Test Tag #3']]


def test_update_tag_page(test_client, db, login_default_user):
    response = test_client.get(url_for('post.tag.update_tag', id=1))
    assert response.status_code == 200
    assert 'Test Tag #1' in response.text


def test_update_tag(test_client, db, login_default_user):
    data = {
        'name': 'Test Tag #10',
        'color': 'PRIMARY'
    }
    response = test_client.post(url_for('post.tag.update_tag_handle', id=1), data=data, follow_redirects=True)
    assert data['name'] in response.text


def test_delete_tag(test_client, db, login_default_user):
    response = test_client.get(url_for('post.tag.delete_tag', id=4), follow_redirects=True)
    assert response.status_code == 200
    assert 'You successfully deleted ur tag.' in response.text
