#!/bin/bash
module load python/3.10.2 cuda/12.2
rm -rf ./.venv
virtualenv --python="/cvmfs/soft.computecanada.ca/easybuild/software/2020/avx2/Core/python/3.10.2/bin/python" .venv
source .venv/bin/activate
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
pip install --upgrade pip
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121
poetry config virtualenvs.options.always-copy true
poetry install -vvv --only-root
