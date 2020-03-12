init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

test_obstacle:
	bash ./scripts/test_obstacle_avoidance.sh

test_autonomy:
	bash ./scripts/test_autonomy.sh

.PHONY: init test run test_obstacle test_autonomy
