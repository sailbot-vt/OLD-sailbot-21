init:
	bash ./scripts/init.sh

test:
	bash ./scripts/test.sh

run:
	bash ./scripts/run.sh

calibrate:
    python3 ./src/buoy_detection/calibration.py

.PHONY: init test run
