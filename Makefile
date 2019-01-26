init:
	pip install virtualenv; \
	virtualenv -p python3.7 p3_7env --no-site-packages; \
	. ./p3_7env/bin/activate; \
	pip install -r requirements.txt

test:
	. ./p3_7env/bin/activate; \
	export ENV test; \
	python -m unittest discover -vcs tests

.PHONY: init test clean
