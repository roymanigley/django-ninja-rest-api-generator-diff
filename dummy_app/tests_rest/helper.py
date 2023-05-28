from django.contrib.auth.models import User

from dummy_app.rest.auth import TokenIssuer


def create_active_user(username='admin', password='admin'):
    return User.objects.create_user(username=username, password=password)


def create_inactive_user(username='admin', password='admin'):
    return User.objects.create_user(username=username, password=password, is_active=False)


def get_token() -> str:
    create_active_user()
    return TokenIssuer.issue_token('admin', 'admin')["token"]
