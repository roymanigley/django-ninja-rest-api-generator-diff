
from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from dummy_app.rest.auth import AuthBearer
from dummy_app.models import Gender
from dummy_app.schemas import GenderSchemaOut, GenderSchemaIn, GenderSchemaInPatch
from dummy_app.rest.helper import apply_audit_infos


def register(api: NinjaAPI) -> None:

    @api.get("gender", response={200: List[GenderSchemaOut]}, auth=AuthBearer())
    def get_genders(request: HttpRequest):
        return Gender.objects.all()

    @api.get("gender/{id}", response={200: GenderSchemaOut}, auth=AuthBearer())
    def get_gender_by_id(request: HttpRequest, id: int):
        return get_object_or_404(Gender, id=id)

    @api.post("gender", response={201: GenderSchemaOut}, auth=AuthBearer())
    def create_gender(request: HttpRequest, payload: GenderSchemaIn):
        payload_dict = apply_audit_infos(payload, request, True)
        record = Gender.objects.create(**payload_dict)
        return record

    @api.put("gender/{id}", response={200: GenderSchemaOut}, auth=AuthBearer())
    def update_gender(request: HttpRequest, id: int, payload: GenderSchemaIn):
        payload_dict = apply_audit_infos(payload, request)
        record = get_object_or_404(Gender, id=id)
        for attr, value in payload_dict.items():
            setattr(record, attr, value)
        record.save()
        return record

    @api.patch("gender/{id}", response={200: GenderSchemaOut}, auth=AuthBearer())
    def update_partial_gender(request: HttpRequest, id: int, payload: GenderSchemaInPatch):
        from_json = json.loads(request.body.decode())
        payload_dict = payload.dict()
        record = get_object_or_404(Gender, id=id)
        for attr, value in from_json.items():
            if attr in payload_dict.keys():
                setattr(record, attr, value if value != 'null' else None)
        payload_dict = apply_audit_infos(payload, request)
        record.save()
        return record

    @api.delete("gender/{id}", response={203: None}, auth=AuthBearer())
    def delete_gender(request, id: int):
        record = get_object_or_404(Gender, id=id)
        record.delete()
        return 203
