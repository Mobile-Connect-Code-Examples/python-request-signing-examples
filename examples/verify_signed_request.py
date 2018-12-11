#!/usr/bin/env python
"""verify_signed_request.py

An example showing the decoding of a signed request object.
"""
from os import path

from jwcrypto.jwk import JWKSet
from jwcrypto.jwt import JWT

import util


def verify_signed_request_example(signed_request_object):
    # Create a store for holding JWKs (e.g. on service startup).
    jwk_store = JWKSet()

    # Import the relevant public key.
    public_key_file_path = environ.get('PUBLIC_KEY_PATH')
    if public_key_file_path is None:
        public_key_file_path = path.join(util.REPO_ROOT, 'keys/public.json')
    public_key_text = util.load_key_text(filepath=public_key_file_path)
    jwk_store.import_keyset(public_key_text)

    # Get the key from the store.
    kid = util.get_kid()
    jwk = jwk_store.get_key(kid)
    jwt = JWT(key=jwk, jwt=signed_request_object)
    # Return the JWT claims (i.e. our raw request object; not to be confused
    # with the 'claims' property possibly included within it).
    return jwt.claims


if __name__ == '__main__':
    from os import environ
    import json

    # The signed request object is loaded from an environment variable. Please
    # ensure:
    # - this is set to the signed request object you want to verify;
    # - the request object was signed using a private key corresponding to the
    #   public key identified by PUBLIC_KEY_PATH.
    signed_request_object = environ.get('SIGNED_REQUEST_OBJECT')
    if signed_request_object is None:
        raise ValueError('Please set SIGNED_REQUEST_OBJECT env var')

    # Removing leading and trailing whitespace.
    signed_request_object = signed_request_object.strip()
    print('Decoding signed request "{}"\n'.format(signed_request_object))

    # Decode the request object.
    text = verify_signed_request_example(signed_request_object)

    # Now parse and re-serialize to make the output clearer.
    request_object = json.loads(text)
    print('Verified request object:\n{}'.format(
        json.dumps(request_object, indent=2)))
