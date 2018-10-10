init:
	source ./p3_7env/bin/activate; \
	pip install -r requirements.txt; \

test:
    export ENV = test; \
	source ./p3_7env/bin/activate; \
	python -m unittest discover -vcs tests; \

.PHONY: init test
