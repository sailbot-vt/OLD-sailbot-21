init:
	source ./p3_7env/bin/activate; \
	pip install -r requirements.txt; \

test:
	source ./p3_7env/bin/activate; \
	export ENV test; \
	python -m unittest discover -vcs tests; \

.PHONY: init test
