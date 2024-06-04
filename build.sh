#!/bin/bash
pylint --recursive=y src
flake8 --max-line-length=120 src
python -m black src
pytest