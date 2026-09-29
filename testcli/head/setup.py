from setuptools import setup

setup(
    name='testcli',
    version='0.1.0',
    packages=['testcli'],
    install_requires=['click', 'pyyaml'],
    entry_points={
        'console_scripts': ['testcli=testcli.cli:main'],
    },
)
