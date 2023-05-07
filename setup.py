import setuptools


setuptools.setup(name="simple_chat_client", version="1.0",
                 packages=[
                    'simple_chat_client',
                 ],
                 install_requires=[
                    'requests~=2.26.0',
                    'dataclass_factory',
                    'textual~=0.23.0',
                    'typing_extensions',
                    'aiohttp~=3.7.4.post0',
                 ],
                 url='#',
                 author='Shapovalov Mihail',
                 author_email='mihailsapovalov05@gmail.com',
                 entry_points={"console_scripts": ["simple_chat_cli = simple_chat_client.ui:cli"]},
                 zip_safe=False)
