.PHONY: install test

install:
	pip3 install -r requirements.txt
	pip3 install -e .

test:
	DJANGO_SETTINGS_MODULE=cbvadmin.tests.test_settings py.test cbvadmin/tests --cov=cbvadmin
