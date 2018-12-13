#!/usr/bin/env python
"""si_example.py

A complete SI request example.
"""
# pylint:disable=invalid-name
from os import environ
import logging

import requests

import util
from sign_request import sign_request_example


logger = logging.getLogger(__name__)


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
    }
    if 'HOST_HEADER' in environ:
        # If using the sandbox locally, you will likely need to set an explicit
        # host header including the operator you are targetting: for example,
        # HOST_HEADER='operator-b.local-sandbox-example.com'
        headers['Host'] = environ['HOST_HEADER']

    logger.info('Making SI authorize request to "%s"', si_auth_url)
    return requests.post(si_auth_url, headers=headers, params=query_params,
                         allow_redirects=False)


if __name__ == '__main__':
    # pylint:disable=invalid-name
    response = send_si_request()
    print('Response:', response)
    print('Body content:', response.content)
