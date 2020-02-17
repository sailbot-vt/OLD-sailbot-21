init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

test_obstacle:
	bash ./scripts/test_obstacle_avoidance.sh

.PHONY: init test run test_obstacle
