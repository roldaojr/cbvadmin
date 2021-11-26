import versioneer
from setuptools import setup

setup(
    name='cbvadmin',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Drop-in replacement of Django admin using Class Based Views',
    long_description=open('README.rst').read(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: JavaScript",
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
    python_requires='>=3.8',
    install_requires=[
        'django>=3.0',
        'django-crispy-forms>=1.10',
        'django-filter>=20.0',
        'django-simple-menu>=1.2',
        'django-tables2>=2.4'
    ]
)
