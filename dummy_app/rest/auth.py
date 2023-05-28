import json
import os
from base64 import b64decode, b64encode
from json import loads, dumps

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.contrib.auth.models import User
from ninja.security import HttpBearer

from datetime import datetime, timedelta

rsa_private_key_path = os.environ.get('RSA_PRIVATE_KEY') or 'rsa_private.pem'
rsa_public_key_path = os.environ.get('RSA_PUBLIC_KEY') or 'rsa_public.pem'

with open(rsa_private_key_path) as f:
    private_key = RSA.importKey(f.read())
    print(private_key)

with open(rsa_public_key_path) as f:
    public_key = RSA.importKey(f.read())
    print(public_key)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> str or None:
        if verify_token(token):
            if is_token_expired(token):
                print(f'token expired: {token}')
                return None
            return token
        else:
            print(f'invalid token: {token}')
            return None


class TokenIssuer(object):

    @staticmethod
    def issue_token(username: str, password: str) -> dict or None:
        user: User = User.objects.get_by_natural_key(username)
        utc_now = datetime.utcnow() + timedelta(minutes=int(os.getenv('TOKEN_EXPIRATION_MINUTES', 60 * 24 * 365)))
        # is_api_user = user.groups.filter(name='API_USER').exists()
        if user is not None and user.check_password(password):
            token_clear = dumps({"username": username, "expiration": utc_now.isoformat()})
            token = b64encode(token_clear.encode('utf-8')).decode('utf-8')
            token = sign_token(token)
            return {"token": token}
        return None


def token_to_dict(token: str) -> dict:
    token = token.split('.')[0]
    token_decoded = b64decode(token.encode('utf-8')).decode('utf-8')
    return loads(token_decoded)


def sign_token(token: str) -> str:
    signer = PKCS1_v1_5.new(private_key)
    hash = SHA512.new(token.encode('utf-8'))
    hash.digest()
    sign = signer.sign(hash)
    return f'{token}.{sign.hex()}'


def verify_token(token: str) -> bool:
    message, signature = token.split('.')
    hash = SHA512.new(message.encode('utf-8'))
    hash.digest()
    verifier = PKCS1_v1_5.new(public_key)
    print(signature)
    return verifier.verify(hash, bytes.fromhex(signature))

def is_token_expired(token: str) -> bool:
    message, signature = token.split('.')
    message_decoded = b64decode(message).decode('utf-8')
    token_expiration = json.loads(message_decoded)["expiration"]
    return datetime.fromisoformat(token_expiration).timestamp() < datetime.utcnow().timestamp()
