./venv/bin/pip install pyarmor.cli.runtime~=3.2.0
./venv/bin/pyarmor gen --recursive --platform windows.x86_64 --platform darwin.x86_64 --platform darwin.arm64 --platform linux.x86_64 -i simple_chat_client/
./venv/bin/python -m build . --skip-dependency-check --no-isolation