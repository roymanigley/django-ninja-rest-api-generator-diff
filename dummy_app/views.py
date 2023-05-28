from ninja import NinjaAPI

from dummy_app.rest import login as rest_login, errors as rest_errors , gender as rest_gender,person as rest_person
api = NinjaAPI()

rest_login.register(api)
rest_errors.register(api)
rest_gender.register(api)
rest_person.register(api)
