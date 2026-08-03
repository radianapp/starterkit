
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def superuser(db):
    user = User.objects.create_superuser('admin@perusahaan.com', 'adminpass', username='admin')
    return user

@pytest.fixture
def regular_user(db):
    user = User.objects.create_user('user@perusahaan.com', 'userpass', username='user')
    return user

@pytest.mark.django_db
class TestUserManagement:
    def test_list_users_as_superuser(self, client, superuser):
        client.force_login(superuser)
        url = reverse('accounts:user_list')
        response = client.get(url)
        assert response.status_code == 200
        assert 'admin@perusahaan.com' in str(response.content)
        
    def test_list_users_as_regular_user(self, client, regular_user):
        client.force_login(regular_user)
        url = reverse('accounts:user_list')
        response = client.get(url)
        assert response.status_code == 403

    def test_add_user_form_shows(self, client, superuser):
        client.force_login(superuser)
        url = reverse('accounts:user_add')
        response = client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_edit_user_form_shows(self, client, superuser, regular_user):
        client.force_login(superuser)
        url = reverse('accounts:user_edit', kwargs={'user_id': regular_user.pk})
        response = client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

