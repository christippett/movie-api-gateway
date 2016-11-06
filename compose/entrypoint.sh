#!/bin/bash

function runTests() {
    cd /app
    echo "CHECKING TYPINGS..."
    mypy app.py
    echo "CHECKING PEP8..."
    pep8 **/*.py
    echo "RUNNING TEST SUITE..."
    pytest
}

if [ "$1" == "test" ]; then
    runTests
    exit 0
else
    /usr/local/bin/gunicorn run:app -w 4 -b 0.0.0.0:5000 --chdir=/app
fi


