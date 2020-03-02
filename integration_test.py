import sys

#from integration_tests.tracking.tracker_integration_test import TrackerTest
#from integration_tests.controls.controls_integration_test import ControlsTest
from integration_tests.autonomy.obstacle_avoidance_integration_test import ObstacleAvoidanceTest

if __name__ == "__main__":
    # get test type
    test_type = sys.argv[1]
    if test_type == 'controls':
        integration_test = ControlsTest()
    elif test_type == 'tracker':
        integration_test = TrackerTest()
    elif test_type == 'obstacle_avoidance':
        integration_test = ObstacleAvoidanceTest()

    integration_test.run()
