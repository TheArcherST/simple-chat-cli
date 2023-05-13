./venv/bin/pip install pyarmor.cli.runtime~=3.2.0
mkdir ./dist
cp ./setup.py ./dist/
cp ./MANIFEST.in ./dist/
./venv/bin/pyarmor gen --recursive --platform windows.x86_64 --platform darwin.x86_64 -i simple_chat_client/
./venv/bin/python -m build ./dist --skip-dependency-check --no-isolation