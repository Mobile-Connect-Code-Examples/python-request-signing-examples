#!/usr/bin/env python
"""si_example.py

A complete SI request example.
"""
from os import environ
from base64 import b64encode

import requests

import util
from sign_request import sign_request_example


def send_si_request():
    """Send an SI request to the sandbox."""
    client_id = util.get_client_id()
    # The URL for the sandbox's si-authorize endpoint.
    si_auth_url = util.require_environment_variable("SI_AUTH_URL")

    # Get the signed request as per the request signing example.
    signed_request = sign_request_example()
    # The complete dict of query parameters.
    query_params = {
        'response_type': 'mc_si_async_code',
        # We'll run an ATP request as part of the example.
        'scope': 'openid mc_atp',
        'request': signed_request,
        'client_id': client_id,
    }

    # The complete dict of headers.
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # This is required in order for this example to run against localhost,
        # as the Sandbox checks the host header in order to determine the
        # operator being used.
        'Host': 'operator-b.local-sandbox-example.com',
    }
    if 'HOST_HEADER' in environ:
        headers['Host'] = environ['HOST_HEADER']

    return requests.post(si_auth_url, headers=headers, params=query_params)


if __name__ == '__main__':
    response = send_si_request()
    print('Response:', response)
    if response.status_code == 200:
        print('Body content:', response.content)
