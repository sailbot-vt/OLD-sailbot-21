HOST = $(shell hostname)

#WRITE ALL CONDITIONALS AND STUFF IN BASH SCRIPT

init:
	
	./install-packages.sh

	pip3 install -r requirements.txt
	pip3 install Adafruit_BBIO

	-mkdir logs

test:
	
	export ENV test; \
	coverage run --source src -m unittest discover -vcs tests

run:
	python3 main.py

.PHONY: init test run
