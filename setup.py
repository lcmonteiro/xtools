# =======================================================================================
# @file: setup.py
# @autor: Luis Monteiro 
# =======================================================================================
# imports
from setuptools import setup, find_packages

# -----------------------------------------------------------------------------
# setup
# -----------------------------------------------------------------------------
setup(
    name='xtranslate',  
    version='0.1',
    author='Luis Monteiro',
    author_email='monteiro.lcm@gmail.com',
    description='',
    packages= find_packages(include=['xtranslate', 'xtranslate/*']),
    install_requires=[
        "openpyxl"
    ],
    entry_points={
        'console_scripts': [
            "translate-xml=xtranslate.translate:main"
        ]
    }
)
# =======================================================================================
# End
# =======================================================================================