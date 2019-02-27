init:
	./install-python.sh

	pip install virtualenv
	virtualenv -p python3.7 p3_7env --no-site-packages

	. ./p3_7env/bin/activate; \
	pip install -r requirements.txt

	-mkdir logs

test:
	. ./p3_7env/bin/activate; \
	export ENV test; \
	coverage run --source src -m unittest discover -vcs tests

run:
	. ./p3_7env/bin/activate; \
	python main.py

.PHONY: init test run
