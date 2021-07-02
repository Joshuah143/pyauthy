from setuptools import setup

setup(
    name='authy',
    version='1.0.0',
    packages=['pyauthy'],
    url='https://github.com/Joshuah143/authy',
    license='GNU GENERAL PUBLIC LICENSE',
    install_requires=[
        'qrcode',
        'twilio'],
    author='Joshua Himmens',
    author_email='joshua.himmens@icloud.com',
    description='A library to make MFA slightly easer to use'
)
