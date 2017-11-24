from setuptools import setup

setup(
    name='hotscreen',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'qrcode'
    ],
)
