from setuptools import setup

setup(
    name='CBVadmin',
    version='0.3.0-alpha1',
    description='Drop-in replacement of Django admin using Class Based Views',
    author='roldaojr',
    author_email='roldaogjr@gmail.com',
    packages=['cbvadmin'],
    include_package_data=True,
    install_requires=[
        'Django>=1.11',
        'django-crispy-forms>=1.6',
        'django-filter>=1.0',
        'django-simple-menu>=1.2',
        'django-tables2>=1.5'
    ]
)
