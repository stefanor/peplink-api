# demands-based PepLink API client

A Python client library for accessing the API of PepWave PepLink
products.

## Scope

Not all API endpoints are implemented, only the ones I needed for my own
personal projects. Contributions of more are welcome!

Currently tested on:

* PepLink MAX BR1 5G

## Development

- clone the repo from Github
- edit code
- create a virtualenv and install the requirements in it.
- run `bin/generate-test-credentials.py` in the virtualenv to create
  integration test credentials.
- run `unittest discover`

## License

Copyright 2023 Stefano Rivera <stefano@rivera.za.net>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
