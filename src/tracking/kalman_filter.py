import numpy as np
import filterpy.kalman as kalman

from src.utils.time_in_millis import time_in_millis

class KalmanFilter():
    def __init__(self, pos, vel, pos_sigma=None, vel_sigma=None):
        """Initialize kalman filter
        Inputs:
            pos -- position of obejct (cartesian)
            vel -- veloicty of obejct (cartesian)
            pos_sigma -- uncretainty of position of obejct (cartesian)
            vel_sigma -- uncertainty of veloicty of obejct (cartesian)
        """

        self.state = np.append(pos, vel)       # create state vector (elements are x, y, v_x, v_y)
        if pos_sigma is None:
            pos_sigma = np.array([3, 3])     # arbitrary choice -- needs tuning
        if vel_sigma is None:
            vel_sigma = np.array([5, 5])     # arbitrary choice -- needs tuning
        self.covar = np.diag(np.append(pos_sigma, vel_sigma))   # create covariance matrix (matrix of certainties of measurements)
        self.measurement_covar = self.covar

        self.process_noise = np.eye(self.state.shape[0])        # initalize process noise

        self.last_time_changed = time_in_millis()
        self.delta_t = 0

        # create state transition matrix
        self.state_trans = np.array([[1., 0, self.delta_t, 0],
                                    [0, 1., 0, self.delta_t],
                                    [0, 0, 1., 0],
                                    [0, 0, 0, 1.]])

        self.measurement_trans = np.eye(self.state.size)    # create measurement transition matrix

    def predict(self):
        """Predicts next state of object
        Side Effects:
            self.state_trans -- calls _update_trans_matrix which updates transition matrix
            self.state -- updates state through kalman predict
            self.covar -- updates uncertainty matrix through kalman predict
        """
        self._update_trans_matrix()  # update state transition matrix with update delta_t
        self._update_process_noise() # update process noise
        self.state, self.covar = kalman.predict(x=self.state, P=self.covar, F=self.state_trans, Q=self.process_noise)

    def update(self, pos, vel, hist_score):
        """Update object position and filter
        Inputs:
            pos -- position of obejct (cartesian)
            vel -- veloicty of obejct (cartesian)
            hist_score -- certainty score based on object history (used as scale factor for measurement covariance) (range 1-2)
        """
        measurement = np.append(pos, vel)
        self.measurement_covar *= hist_score

        self.state, self.covar = kalman.update(x=self.state, P=self.covar, z=measurement, R=self.measurement_covar, H=self.measurement_trans)
        
    def _update_trans_matrix(self):
        """Updates transition matrix for time delta since last prediction
        Side Effects:
            self.state_trans -- updates velocity coefficients in position equations
            self.last_time_changed -- updates last time changed to reflect that state has changed
            self.delta_t -- updates delta between current time and last time changed (used for predict)
        """
        self.delta_t = (time_in_millis() - self.last_time_changed) / 1000.

        # update delta_t in state transition matrix
        self.state_trans[0, 2] = self.delta_t
        self.state_trans[1, 3] = self.delta_t

        self.last_time_changed = time_in_millis()

    def _update_process_noise(self):
        """
        Updates process noise using distance from origin of object
        Side Effects:
            self.process_noise -- updates using range
        """
        # bearing noise increases as distance from origin DECREASES (small changes in position result in large bearing changes)
        bearing_scale_fac = 15. / self.state[0]         # arbitrary choice for numerator
        self.process_noise[0::2, :] *= bearing_scale_fac
