import datetime
from datetime import datetime

from dummy_app.rest.auth import token_to_dict


def apply_audit_infos(payload, request, create=False):
    payload_dict = payload.dict()
    token = request.headers.get('Authorization')[7:].split('.')[0]
    username = token_to_dict(token)['username']
    if create:
        payload_dict['creator'] = username
        payload_dict['create_date'] = datetime.utcnow()
    payload_dict['modifier'] = username
    payload_dict['modified_date'] = datetime.utcnow()
    return payload_dict
