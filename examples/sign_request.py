#!/usr/bin/env python
"""sign_request.py

An example showing the signing of a request object.
"""
from os import environ, path

from jwcrypto.jwk import JWKSet

import util


def sign_request_example():
    """Example: sign a request object.

    Loads the request object fields from environment variables and produces the
    signed JWT as text.
    """
    # Create a store for holding JWKs (e.g. on service startup).
    jwk_store = JWKSet()

    # Import the relevant private key.
    private_key_file_path = environ.get('PRIVATE_KEY_PATH')
    if private_key_file_path is None:
        private_key_file_path = path.join(util.REPO_ROOT, 'keys/private.json')
    private_key_text = util.load_key_text(filepath=private_key_file_path)
    jwk_store.import_keyset(private_key_text)

    # Create an example request object.
    raw_request_object = util.get_raw_request_object()

    # Get a key from the JWK store, and use it to sign the request object.
    kid = util.get_kid()
    jwk = jwk_store.get_key(kid)
    jwt_as_text = util.sign_request(jwk, raw_request_object)
    return jwt_as_text


if __name__ == '__main__':
    print(sign_request_example())
