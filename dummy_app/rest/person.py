
from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from dummy_app.rest.auth import AuthBearer
from dummy_app.models import Person
from dummy_app.schemas import PersonSchemaOut, PersonSchemaIn, PersonSchemaInPatch
from dummy_app.rest.helper import apply_audit_infos


def register(api: NinjaAPI) -> None:

    @api.get("person", response={200: List[PersonSchemaOut]}, auth=AuthBearer())
    def get_persons(request: HttpRequest):
        return Person.objects.all()

    @api.get("person/{id}", response={200: PersonSchemaOut}, auth=AuthBearer())
    def get_person_by_id(request: HttpRequest, id: int):
        return get_object_or_404(Person, id=id)

    @api.post("person", response={201: PersonSchemaOut}, auth=AuthBearer())
    def create_person(request: HttpRequest, payload: PersonSchemaIn):
        payload_dict = apply_audit_infos(payload, request, True)
        record = Person.objects.create(**payload_dict)
        return record

    @api.put("person/{id}", response={200: PersonSchemaOut}, auth=AuthBearer())
    def update_person(request: HttpRequest, id: int, payload: PersonSchemaIn):
        payload_dict = apply_audit_infos(payload, request)
        record = get_object_or_404(Person, id=id)
        for attr, value in payload_dict.items():
            setattr(record, attr, value)
        record.save()
        return record

    @api.patch("person/{id}", response={200: PersonSchemaOut}, auth=AuthBearer())
    def update_partial_person(request: HttpRequest, id: int, payload: PersonSchemaInPatch):
        from_json = json.loads(request.body.decode())
        payload_dict = payload.dict()
        record = get_object_or_404(Person, id=id)
        for attr, value in from_json.items():
            if attr in payload_dict.keys():
                setattr(record, attr, value if value != 'null' else None)
        payload_dict = apply_audit_infos(payload, request)
        record.save()
        return record

    @api.delete("person/{id}", response={203: None}, auth=AuthBearer())
    def delete_person(request, id: int):
        record = get_object_or_404(Person, id=id)
        record.delete()
        return 203
