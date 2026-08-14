"""
Test untuk authorization mixins dan decorators.
US-020: Authorization (Permission & Group)
"""

import pytest
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.views.generic import TemplateView

from apps.core.decorators import group_required, role_required
from apps.core.mixins import MultiplePermissionsRequiredMixin, RoleRequiredMixin

# ─── Fixtures ───────────────────────────────────────────────────


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture
def admin_group(db):
    return Group.objects.create(name="Admin")


@pytest.fixture
def manager_group(db):
    return Group.objects.create(name="Manager")


# ─── MultiplePermissionsRequiredMixin ───────────────────────────


class _PermView(MultiplePermissionsRequiredMixin, TemplateView):
    template_name = "errors/403.html"
    permissions_required = ["accounts.view_user"]


@pytest.mark.django_db
def test_multiple_perms_unauthenticated_redirects(rf, django_user_model):
    view = _PermView.as_view()
    request = rf.get("/")
    request.user = type("AnonUser", (), {"is_authenticated": False})()
    response = view(request)
    # AccessMixin.handle_no_permission → redirect ke login
    assert response.status_code == 302


@pytest.mark.django_db
def test_multiple_perms_no_perm_raises_403(rf, django_user_model):
    user = django_user_model.objects.create_user(
        email="noauth@test.com", password="x", username="noauth@test.com"
    )
    view = _PermView.as_view()
    request = rf.get("/")
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request)


@pytest.mark.django_db
def test_multiple_perms_with_perm_passes(rf, django_user_model):
    user = django_user_model.objects.create_user(
        email="auth@test.com", password="x", username="auth@test.com"
    )
    perm = Permission.objects.get(codename="view_user", content_type__app_label="accounts")
    user.user_permissions.add(perm)
    # Refresh dari DB supaya perm cache clear
    user = django_user_model.objects.get(pk=user.pk)
    view = _PermView.as_view()
    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.status_code == 200


# ─── RoleRequiredMixin ──────────────────────────────────────────


class _RoleView(RoleRequiredMixin, TemplateView):
    template_name = "errors/403.html"
    role_required = "Admin"


@pytest.mark.django_db
def test_role_mixin_wrong_group_raises_403(rf, django_user_model, admin_group, manager_group):
    user = django_user_model.objects.create_user(
        email="mgr@test.com", password="x", username="mgr@test.com"
    )
    user.groups.add(manager_group)
    view = _RoleView.as_view()
    request = rf.get("/")
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request)


@pytest.mark.django_db
def test_role_mixin_correct_group_passes(rf, django_user_model, admin_group):
    user = django_user_model.objects.create_user(
        email="adm@test.com", password="x", username="adm@test.com"
    )
    user.groups.add(admin_group)
    view = _RoleView.as_view()
    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_role_mixin_superuser_always_passes(rf, django_user_model):
    user = django_user_model.objects.create_superuser(
        email="super@test.com", password="x", username="super@test.com"
    )
    view = _RoleView.as_view()
    request = rf.get("/")
    request.user = user
    response = view(request)
    assert response.status_code == 200


# ─── group_required decorator ───────────────────────────────────


@pytest.mark.django_db
def test_group_required_wrong_group_raises_403(rf, django_user_model, manager_group):
    @group_required("Admin")
    def my_view(request):
        return type("R", (), {"status_code": 200})()

    user = django_user_model.objects.create_user(
        email="u@test.com", password="x", username="u@test.com"
    )
    user.groups.add(manager_group)
    request = rf.get("/")
    request.user = user
    with pytest.raises(PermissionDenied):
        my_view(request)


@pytest.mark.django_db
def test_group_required_correct_group_passes(rf, django_user_model, admin_group):
    @group_required("Admin")
    def my_view(request):
        return type("R", (), {"status_code": 200})()

    user = django_user_model.objects.create_user(
        email="u2@test.com", password="x", username="u2@test.com"
    )
    user.groups.add(admin_group)
    request = rf.get("/")
    request.user = user
    result = my_view(request)
    assert result.status_code == 200


@pytest.mark.django_db
def test_role_required_accepts_string(rf, django_user_model, admin_group):
    @role_required("Admin")
    def my_view(request):
        return type("R", (), {"status_code": 200})()

    user = django_user_model.objects.create_user(
        email="u3@test.com", password="x", username="u3@test.com"
    )
    user.groups.add(admin_group)
    request = rf.get("/")
    request.user = user
    result = my_view(request)
    assert result.status_code == 200


@pytest.mark.django_db
def test_group_required_superuser_passes(rf, django_user_model):
    @group_required("Admin")
    def my_view(request):
        return type("R", (), {"status_code": 200})()

    user = django_user_model.objects.create_superuser(
        email="sup@test.com", password="x", username="sup@test.com"
    )
    request = rf.get("/")
    request.user = user
    result = my_view(request)
    assert result.status_code == 200
