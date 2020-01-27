init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: init test run test_controls
