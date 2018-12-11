"""Example utilitites."""
from os import environ, path
import logging
import json

from jwcrypto.jwt import JWT


# pylint:disable=invalid-name
logger = logging.getLogger(__name__)


REPO_ROOT = path.dirname(path.dirname(__file__))


def load_key_text(filepath=''):
    """Load the text from a private key file.

    Args:
        filepath (str): the filepath to load from. Defaults to the environment
            variable PRIVATE_KEY_FILE. If this is not set, raises ValueError.
    """
    if not filepath:
        raise ValueError('Invalid filepath', filepath)
    if not path.isfile(filepath):
        raise ValueError('Path "%s" does not point to a file', filepath)
    logger.debug('Loading key text from %s', filepath)
    with open(filepath, 'r') as private_key_file:
        return private_key_file.read()


def get_inputs():
    """Get input values for running examples.

    Attempts to read values from environment variables; where not found,
    sensible defaults are used.
    """
    client_id = environ.get(
        'CLIENT_ID', 'x-a94d903f-ad45-4135-80b8-ac459f41b38f')
    return {
        'response_type': environ.get('RESPONSE_TYPE', 'mc_si_async_code'),
        'kid': environ.get('KID', 'developer-app'),
        'scope': environ.get('scope', 'openid mc_atp'),
        'client_id': client_id,
        'version': environ.get('VERSION', 'mc_si_r2_v1.0'),
        'nonce': environ.get('NONCE', '878aacd7-83f1-4b4f-9582-7347b0a6fa62'),
        'login_hint': environ.get('LOGIN_HINT', 'MSISDN:447700900907'),
        'acr_values': int(environ.get('ACR_VALUES', '3')),
        'client_notification_token': environ.get(
            'CLIENT_NOTIFICATION_TOKEN',
            'Wm1VFlURXpNR1V0T0Rjek1TMDBOVFpqTFdGalpEZ3'),
        'notification_uri': environ.get(
            'NOTIFICATION_URI' 'https://mc.example.com/callback'),
        'iss': environ.get('ISS', client_id),
        'aud': environ.get('AUD', 'https://operator.example.com'),

        # Optional request object parameters.
        'claims': (json.loads(environ['claims']) if 'claims' in environ else {
            "premiuminfo": {
                "address": {
                    "value": "123 Fake Street",
                },
            },
        }),
    }


REQUEST_OBJECT_REQUIRED_KEYS = (
    'response_type',
    'client_id',
    'scope',
    'version',
    'nonce',
    'login_hint',
    'acr_values',
    'client_notification_token',
    'notification_uri',
    'iss',
    'aud',
)


def get_raw_request_object(overrides=None):
    """Get a raw (unsigned) request object."""
    inputs = get_inputs()
    if overrides:
        inputs.update(overrides)
    return {key: inputs[key] for key in REQUEST_OBJECT_REQUIRED_KEYS}


def sign_request(jwk, raw_request_object):
    """Sign a raw request object.

    Args:
        jwk (JWK): the JWK used for signing.
        raw_request_object (dict): the raw request object, as a dict.
    """
    logger.debug('Signing request %s', raw_request_object)
    if jwk.key_type != 'RSA':
        raise ValueError('This example only supports RSA256')
    header = {
        'alg': 'RS256',
        'typ': 'JWT',
        'kid': jwk.key_id,
    }
    logger.debug('Header: %s', header)
    jwt = JWT(header=header, claims=raw_request_object)
    jwt.make_signed_token(jwk)
    return jwt.serialize()
