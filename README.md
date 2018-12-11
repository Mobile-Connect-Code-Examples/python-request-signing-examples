# python-request-signing-examples
Python code examples for the Server Initiated Request Object.

## Installation
Create a virtualenv and install requirements from the requirements file:

    pip install -r requirements.txt

## Examples
The following examples are provided.

-   [examples/generate_keys.py](examples/generate_keys.py): this script creates
    public and private JWKs. As well as being useful for the sake of
    demonstration, these keys can be used in the other examples.

-   [examples/sign_request.py](examples/sign_request.py): an example script
    which uses the generated private key to sign a request object.

-   [examples/verify_signed_request.py](examples/verify_signed_request.py):
    this demonstrates the verification of signed request objects.

-   [examples/si_example.py](examples/si_example.py): this final example builds
    on the request signing example to construct a valid SI request.
