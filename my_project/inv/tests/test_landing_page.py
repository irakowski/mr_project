import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


def test_landing_page(client):
   """
   Verify that landing page renders as expected
   """
   url = reverse('landing-page')
   response = client.get(url)
   assert response.status_code == 200
   
@pytest.mark.parametrize('view_name', ['register', 'login'])
def test_accessability(view_name, client):
   """
   Verify that the registration and login view are publicly accessible
   """
   url = reverse(view_name)
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_register(client):
    """Registers a user a verifies if the user was created"""
    register_url = reverse('register')
    response = client.post(register_url, {
        'username': 'test_username',
        'email': 'testuser@test.com',
        'first_name': 'MyName',
        'last_name':'LastName',
        'password1': 'test_password_4878',
        'password2': 'test_password_4878'
    })

    # The registration view should redirect
    assert response.status_code == 302
    assert response.url == reverse('create-company-profile')

    # There should be a user with 'my_username'
    user = User.objects.get(username='test_username')
    assert user in User.objects.all()


@pytest.mark.django_db
def test_login_and_logout(client):
    """Tests logging in and logging out"""
    # Create a fake user
    user = User(username='test_username_2')
    user.set_password('test2_password4878')
    user.save()

    login_url = reverse('login')
    response = client.post(login_url, {
        'username': 'test_username_2',
        'password': 'test2_password4878'
    })

    # The login url should redirect to the dashboard
    assert response.status_code == 302
    assert response.url == reverse('main')

    # Logged in users have a session created for them
    assert Session.objects.count() == 1

    # Log out the user
    logout_url = reverse('logout')
    response = client.get(logout_url)

    # The logout view redirects to the landing page
    assert response.status_code == 302
    assert response.url == reverse('landing-page')

    # There should be no more sessions left after logging out
    assert not Session.objects.exists()