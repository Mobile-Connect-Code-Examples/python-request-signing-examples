#!/usr/bin/env python
"""A script demonstrating creation of signed request object for SI auth.

Either execute this script to print out example query parameters and JWT, or
import it and use the functions defined below.

A number of environment variable options are accepted. Please see
..py:ref:`get_inputs` for details.
"""
from os import path, environ
import sys
import json
import logging

import requests
from jwcrypto.jwk import JWKSet
from jwcrypto.jwt import JWT


logger = logging.getLogger(__name__)


examples_dir = path.dirname(path.dirname(path.abspath(__file__)))
private_key_path = environ.get(
    'PRIVATE_KEY_PATH', path.join(examples_dir, 'keys/private.json'))
logger.debug('Private key path: %s', private_key_path)


if not path.exists(private_key_path):
    logger.fatal(
        "Key file '%s' does not exist. Please generate a key file first, "
        "for example by running `examples/generate-key.py`.",
        private_key_path)
    sys.exit(1)


# Load the private key used for signing from a file.
jwk_store = JWKSet()
with open(private_key_path, 'r') as private_key_file:
    jwk_store.import_keyset(private_key_file.read())


def send_request(endpoint_url, kid, response_type, **request_obj_kwargs):
    """Send an SI authorize request.

    Args:
        endpoint_url (str): the endpoint URL, e.g.
            'https://service-provider.com/oidc/si-authorize'.
        kid (str): the 'kid' (key ID) of the JWE.
        response_type (str): the response type.
        request_obj_kwargs (dict): any kwargs to insert into the request
            object before signing.
    """
    logger.debug('send_request(%s, %s, %s, %s)', endpoint_url, kid,
                 response_type, **request_obj_kwargs)
    return requests.post(
        endpoint_url,
        params=construct_query_params(
            kid=kid, response_type=response_type, **request_obj_kwargs))


def construct_query_params(kid, response_type, **request_obj_kwargs):
    """Construct query parameters for an SI authorize request.

    Args:
        kid (str): the 'kid' (key ID) of the JWE.
        response_type (str): the response type.
        request_obj_kwargs (dict): any kwargs to insert into the request
            object before signing.
    """
    logger.debug('construct_query_params(%s, %s, %s)',
                 kid, response_type, **request_obj_kwargs)
    return {
        'scope': request_obj_kwargs['scope'],
        'client_id': request_obj_kwargs['client_id'],
        'response_type': response_type,
        'request': construct_jwt(kid, **request_obj_kwargs),
    }


def construct_jwt(kid, **request_obj_kwargs):
    """Construct the request object JWT.

    Args:
        request_obj_kwargs (dict): any values to insert into the request object
            before signing.
    """
    logger.debug('construct_jwt(%s, %s)', kid, request_obj_kwargs)
    jwk = jwk_store.get_key(kid)
    if jwk is None:
        raise ValueError('No JWK found for kid', kid)
    # For simplicity we're assuming only the recommended algorithm, RSA256.
    if jwk.key_type != 'RSA':
        raise ValueError('This example only supports RSA encryption')
    header = dict(alg='RS256', typ='JWT', kid=jwk.key_id)
    jwt = JWT(header=header, claims=request_obj_kwargs)
    jwt.make_signed_token(jwk)
    signed = jwt.serialize()
    return signed


def get_inputs():
    """Get input values for the script.

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


if __name__ == '__main__':
    input_values = get_inputs()

    # Construct the query parameters (in particular sign the request object).
    query_params = construct_query_params(**input_values)
    print('Query params:\n{}\n'.format(json.dumps(query_params, indent=4)))

    # Now decode the key and retrieve the claims.
    token_id = input_values['kid']
    jwt = JWT(key=jwk_store.get_key(token_id), jwt=query_params['request'])
    print('JWT claims:\n{}'.format(jwt.claims))
