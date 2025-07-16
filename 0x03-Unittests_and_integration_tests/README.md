# GitHub Org Client - Unittests and Integration Tests

This project provides a simulated GitHub organization client built with Python 3.7. It includes:

- Utility functions for working with nested maps and HTTP JSON requests
- A client (`GithubOrgClient`) to interact with GitHub-like APIs
- Structured unit tests using `unittest` and `parameterized`
- Test fixtures for mocking API responses

## Features

- Pure Python 3.7 (runs on Ubuntu 18.04 LTS)
- Type-annotated functions and methods
- Fully documented modules, classes, and functions
- Compliant with `pycodestyle` (version 2.5)
- All files are executable and follow the `#!/usr/bin/env python3` convention
- Unit tests use mocking (`unittest.mock`) to avoid external HTTP requests


## Running Tests

Ensure dependencies are installed:
```bash
pip3 install requests parameterized
