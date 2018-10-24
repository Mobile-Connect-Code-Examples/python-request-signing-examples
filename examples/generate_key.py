#!/usr/bin/env python
"""A script demonstrating creation of public and private keys.

Either execute this script to create public & private key files, or import it
and use the variables defined below.

Accepts the following environment variables.

*   KEYS_DIR - the directory in which to store key files.
*   KID - the 'kid' field to use in creating JWKs.
"""
import os
import json

from jwcrypto.jwk import JWK


keys_dir = os.environ.get('KEYS_DIR') or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'keys')
kid = os.environ.get('KID', 'developer-app')


key = JWK.generate(kty='RSA', size=2048, kid='developer-app')


private_contents = {
    'keys': [
        json.loads(key.export_private()),
     ],
}
public_contents = {
    'keys': [
        json.loads(key.export_public()),
    ],
}


if __name__ == '__main__':
    if not os.path.exists(keys_dir):
        os.mkdir(keys_dir)

    with open(os.path.join(keys_dir, 'private.json'), 'w') as key_file:
        json.dump(private_contents, key_file)

    with open(os.path.join(keys_dir, 'public.json'), 'w') as key_file:
        json.dump(public_contents, key_file)
