import math
import functools

import numpy
import scipy


# THIS IS BROKEN, DO NOT USE #


def predict_velocity(world, t, boat, direction, velocity_config):
    """Predicts the velocity.

    Keyword arguments:
    world -- The world in which to predict the velocity
    t -- The time at which to predict the velocity
    boat -- The boat for which to estimate the velocity
    dir -- The true wind angle of the boat
    velocity_config -- The configuration options for the velocity predictor

    Returns:
    A PredictVelocityResult with fields
        - Speed through water (stw)
            The speed of the hull through the water (not considering current)
        - Velocity made good (vmg)
            The upwind component of the velocity
        - Heel angle
    """
    # Initial guess for velocity
    v_hs = 1.25 * math.sqrt(boat.lwl)  # 1.25 is hull speed coefficient for m/s

    # Get world data
    v_tw = world.true_wind_at_time(t)

    # Start value for minimizer
    x0 = [v_hs, 0, 0, 1] if v_tw > v_hs else [v_tw, 0, 0, 1]
    bounds = scipy.optimize.Bounds([velocity_config.min_v,
                                    velocity_config.min_phi,
                                    velocity_config.min_b,
                                    velocity_config.min_f],
                                   [velocity_config.max_v,
                                    velocity_config.max_phi,
                                    velocity_config.max_b,
                                    velocity_config.max_f])

    def x_constrain(x):
        return constrain(x, v_tw, direction, world, boat)

    scipy.optimize.minimize(vel_foo, x0, bounds=bounds,
                            constraints=scipy.optimize.NonlinearConstraint(x_constrain),
                            options={
                                "maxiter": 1000,
                                "disp": False
                            })
