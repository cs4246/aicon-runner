#!/bin/bash

set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PYTHON=$1/bin/python
PYTHON_VERSION=$($PYTHON --version | cut -d' ' -f2- | cut -d'.' -f1,2)

$PYTHON -m venv --copies "$2"
realpath "$1/lib/python$PYTHON_VERSION/site-packages" > "$2/lib/python$PYTHON_VERSION/site-packages/base_venv.pth"
source "$2/bin/activate"

python -m pip install --upgrade pip

for i in "${@:3}"; do
    python -m pip install --no-cache-dir "$i"
done

deactivate
