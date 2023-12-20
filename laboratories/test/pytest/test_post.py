from flask import url_for

from app.domain.Post import Post


def test_get_post(test_client, db, login_default_user):
    response = test_client.get(url_for('post.get_post', id=1), follow_redirects=True)
    assert response.status_code == 200
    assert 'Test post #1' in response.text


def test_get_all_posts(test_client, db, login_default_user):
    response = test_client.get(url_for('post.post_list'))
    assert response.status_code == 200
    assert 'Test post #1' in response.text
    assert 'Test post #2' in response.text
    assert 'Next' in response.text


def test_get_all_posts_with_pagination(test_client, db, login_default_user):
    response = test_client.get(url_for('post.post_list', page=2))
    assert response.status_code == 200
    assert 'Test post #3' in response.text
    assert 'Previous' in response.text


def test_create_post_page(test_client, db, login_default_user):
    response = test_client.get(url_for('post.create_post'))
    assert response.status_code == 200
    assert 'Test Tag #1' in response.text


def test_create_post(test_client, db, login_default_second_user):
    data = {
        'title': 'Test post #4',
        'text': 'Some  text',
        'type': 'NEWS',
        'categories': 1,
        'tags': ['Test Tag #1', 'Test Tag #2'],
        'enabled': True
    }
    created_response = test_client.post(url_for('post.create_post_handle'), data=data, follow_redirects=True)
    assert created_response.status_code == 200

    post = Post.query.get(4)
    assert post


def test_access_edit_post(test_client, db, login_default_second_user):
    response = test_client.get(url_for('post.post_list'))
    assert response.status_code == 200
    assert 'Test post #1' in response.text
    assert 'Edit...' not in response.text
    assert 'Delete...' not in response.text


def test_update_post(test_client, db, login_default_user):
    data = {
        'title': 'Test post #1',
        'text': 'Some Text #2',
        'type': 'NEWS',
        'categories': 1,
        'tags': [],
        'enabled': True
    }
    updated_response = test_client.post(url_for('post.update_post_handle', id=1), data=data, follow_redirects=True)
    assert updated_response.status_code == 200

    response = test_client.get(url_for('post.get_post', id=1))
    assert response.status_code == 200
    assert data['text'] in response.text


def test_delete_post(test_client, db, login_default_user):
    response = test_client.get(url_for('post.delete_post', id=1), follow_redirects=True)
    assert response.status_code == 200
    assert 'You successfully deleted ur post.' in response.text
    assert 'Test post #2' in response.text
