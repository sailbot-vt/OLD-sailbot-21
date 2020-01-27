init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

clean:
	rm logs/*

.PHONY: init test run clean
