init:
	source ./p3_6env/bin/activate; \
	pip install -r requirements.txt; \

test:
	source ./p3_6env/bin/activate; \
	python -m unittest discover -vcs tests; \

.PHONY: init test
