ROOT_DIR = $(shell pwd)

init:
	# Set up Python virtual environment
	pip install virtualenv; \
	virtualenv -p python3.7 p3_7env --no-site-packages; \
	source ./p3_7env/bin/activate; \

	# Install Python dependencies
	pip install -r requirements.txt; \

	# Build msg library
	cd src/msg && $(MAKE) build; \

	# Build msg tests
	-mkdir bin; \
	cd $(ROOT_DIR)/tests/msg_tests/c_tests && $(MAKE) build ROOT_DIR=$(ROOT_DIR); \

test:
	source ./p3_7env/bin/activate; \
	export ENV test; \
	python -m unittest discover -vcs tests; \
	cd tests/msg_tests/c_tests && $(MAKE) test ROOT_DIR=$(ROOT_DIR); \

clean:
	cd src/msg && $(MAKE) build; \

.PHONY: init test clean
