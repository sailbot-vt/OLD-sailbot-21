init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

clean:
	rm logs/*

test_obstacle:
	bash ./scripts/test_obstacle_avoidance.sh

test_autonomy:
	bash ./scripts/test_autonomy.sh

test_tracker:
	bash ./scripts/test_tracker.sh

test_controls:
	bash ./scripts/test_controls.sh

.PHONY: init test run clean test_tracker test_controls test_obstacle test_autonomy
