import setuptools


setuptools.setup(name="simple_chat_cli", version="1.0",
                 install_requires=open('requirements.txt').read().splitlines(),
                 url='#',
                 author='Shapovalov Mihail',
                 author_email='mihailsapovalov05@gmail.com',
                 entry_points={"console_scripts": ["simple-chat-client = simple_chat_client.ui:cli"]},
                 zip_safe=False)
