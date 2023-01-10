import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def register_url():
    return reverse('register')

def test_register_view_get(client, register_url):
    response = client.get(register_url)
    assert response.status_code == 200
    assert 'register.html' in (t.name for t in response.templates)
    assert 'form' in response.context

def test_register_view_post_valid_data(client, register_url):
    response = client.post(register_url,
                           {'username': 'testuser',
                            'first_name': 'test',
                            'last_name': 'user',
                            'email': 'testuser@example.com',
                            'password1': 'password123',
                            'password2': 'password123'
                            })
    assert response.status_code == 302
    assert response.url == reverse('login')
    assert User.objects.count() == 1
    user = User.objects.first()
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.first_name == 'test'
    assert user.last_name == 'user'

def test_register_view_post_invalid_data(client, register_url):
    response = client.post(register_url,
                           {'username': '',
                            'first_name': '',
                            'last_name': '',
                            'email': '',
                            'password1': 'password123',
                            'password2': 'password456'
                            })
    assert response.status_code == 200
    assert 'register.html' in (t.name for t in response.templates)
    assert 'form' in response.context
    assert not response.context['form'].is_valid()
    assert User.objects.count() == 0

