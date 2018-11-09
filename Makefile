init:
	source ./p3_7env/bin/activate; \
	pip install -r requirements.txt; \
	cd src/msg_system && $(MAKE) build; \

test:
	source ./p3_7env/bin/activate; \
	export ENV test; \
	python -m unittest discover -vcs tests; \

clean:
	cd src/msg && $(MAKE) build; \

.PHONY: init test clean
