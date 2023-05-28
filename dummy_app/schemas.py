from typing import Optional

from ninja import Schema
from datetime import date, datetime
from dummy_app.models import Status

class GenderSchemaIn(Schema):
    designation: str


class GenderSchemaInPatch(Schema):
    designation: Optional[str]


class GenderSchemaOut(Schema):
    id: int
    designation: str
    creator: str
    create_date: datetime
    modifier: str
    modified_date: datetime


class PersonSchemaIn(Schema):
    first_name: str
    description: str
    height: int
    birth_date: date
    state: Status
    gender_id: Optional[int]


class PersonSchemaInPatch(Schema):
    first_name: Optional[str]
    description: Optional[str]
    height: Optional[int]
    birth_date: Optional[date]
    state: Optional[Status]
    gender_id: Optional[int]


class PersonSchemaOut(Schema):
    id: int
    first_name: str
    description: str
    height: int
    birth_date: date
    state: Status
    gender: Optional[GenderSchemaOut]
    creator: str
    create_date: datetime
    modifier: str
    modified_date: datetime


