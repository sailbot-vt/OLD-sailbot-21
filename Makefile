init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

test_tracker:
	bash ./scripts/test_tracker.sh

.PHONY: init test run test_tracker
