from setuptools import setup

setup(
    name='enki',
    version='0.1.0',
    packages=['enki', 'enkicli'],
    entry_points={
        'console_scripts': [
            'enki = enkicli.__main__:main'
        ]
    })
