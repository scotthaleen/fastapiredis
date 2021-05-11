#!/usr/bin/env bash

set -x

mypy --show-error-codes app
black --line-length 119 app --check
isort --check-only app
flake8
