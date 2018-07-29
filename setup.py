import re
from setuptools import setup

# get version without importing
with open('cbvadmin/__init__.py', 'rb') as f:
    VERSION = str(re.search('__version__ = \'(.+?)\'', f.read().decode('utf-8')).group(1))

setup(
    name='CBVadmin',
    version=VERSION,
    description='Drop-in replacement of Django admin using Class Based Views',
    long_description=open('README.rst').read(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=['admin', 'django'],
    author='roldaojr',
    author_email='roldaogjr@gmail.com',
    url='https://github.com/roldaojr/cbvadmin',
    license='LGPL',
    packages=['cbvadmin'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    install_requires=[
        'Django>=2.0',
        'django-crispy-forms>=1.6',
        'django-filter>=1.0',
        'django-simple-menu>=1.2',
        'django-tables2>=1.5'
    ]
)
