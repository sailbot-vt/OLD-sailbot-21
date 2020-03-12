import sys

#from integration_tests.tracking.tracker_integration_test import TrackerTest
#from integration_tests.controls.controls_integration_test import ControlsTest
from integration_tests.autonomy.obstacle_avoidance_integration_test import ObstacleAvoidanceTest
from integration_tests.autonomy.autonomy_integration_test import AutonomyTest

if __name__ == "__main__":
    # get test type
    test_type = sys.argv[1]
    if test_type == 'controls':
        integration_test = ControlsTest()
    elif test_type == 'tracker':
        integration_test = TrackerTest()
    elif test_type == 'obstacle_avoidance':
        integration_test = ObstacleAvoidanceTest()
    elif test_type == 'autonomy':
        integration_test = AutonomyTest()

    integration_test.run()
