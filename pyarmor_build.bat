./venv/bin/pip install pyarmor.cli.runtime~=3.2.0
./venv/bin/pyarmor gen --recursive --platform windows.x86_64 --platform darwin.x86_64 --platform darwin.arm64 --platform linux.x86_64 -i simple_chat_client
mv setup.cfg plain_setup.cfg
mv pyarmor_setup.cfg setup.cfg
./venv/bin/python -m build . --skip-dependency-check --no-isolation
mv setup.cfg pyarmor_setup.cfg
mv plain_setup.cfg setup.cfg