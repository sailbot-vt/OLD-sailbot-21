import sys

from integration_tests.tracking.tracker_integration_test import TrackerTest
#from integration_tests.controls.controls_integration_test import ControlsTest

if __name__ == "__main__":
    # get test type
    test_type = sys.argv[1]
    if test_type == 'controls':
        integration_test = ControlsTest()
    elif test_type == 'tracker':
        integration_test = TrackerTest()

    integration_test.run()
