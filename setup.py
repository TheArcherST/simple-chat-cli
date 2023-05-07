import setuptools


setuptools.setup(name="simple_chat_cli", version="1.0",
                 packages=setuptools.find_packages(),
                 url='#',
                 author='Shapovalov Mihail',
                 author_email='mihailsapovalov05@gmail.com',
                 entry_points={"console_scripts": ["simple-chat-client = simple_chat_client.main:cli"]},
                 zip_safe=False)
