from django.http import HttpRequest
from ninja import NinjaAPI

from dummy_app.rest.auth import TokenIssuer


def register(api: NinjaAPI) -> None:

    @api.post("/login", auth=None, response={200: dict, 401: dict})
    def get_token(request: HttpRequest, username: str, password: str):
        token: dict or None = TokenIssuer.issue_token(username, password)
        if token is not None:
            return 200, token
        else:
            return 401, {'error': 'access denied'}

