from django.http import HttpRequest
from ninja import NinjaAPI

from django.db.utils import IntegrityError
from ninja.errors import ValidationError, AuthenticationError, HttpError


def register(api: NinjaAPI):

    @api.exception_handler(ValidationError)
    def handle_validation_error(request: HttpRequest, e: ValidationError):
        print(e)
        return api.create_response(request, {"status": "error", "detail": str(e)}, status=400)

    @api.exception_handler(IntegrityError)
    def handle_integrity_error(request: HttpRequest, e: IntegrityError):
        print(e)
        return api.create_response(request, {"status": "error", "detail": str(e)}, status=500)

    @api.exception_handler(Exception)
    def handle_general_error(request: HttpRequest, e: Exception):
        print(e)
        return api.create_response(request, {"status": "error", "detail": str(e)}, status=500)
