# Rusty Bois

# Development Setup
## Requirements
- Python 3.7

## Setting up the dev environment
1. create and activate a python virtual environment e.g.
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
    or with your favourite virtual environment managment tool
2. Install poetry
    ```shell
    pip install -U poetry
    ```
3. Install required dependencies
    ```shell
    poetry install
    ```

## Makefile
There's a Makefile at the root of the project directory. Run `make help`
to see a list of available make targets.

## Pre-Commit
Before commiting, please make sure all tests pass (make tests) and
your code is properly formatted (make format)