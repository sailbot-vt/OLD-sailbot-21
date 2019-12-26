import numpy as np
import filterpy.kalman as kalman

from datetime import datetime as dt

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
            pos_sigma = np.array([20, 20])     # arbitrary choice -- needs tuning
        if vel_sigma is None:
            vel_sigma = np.array([50, 50])     # arbitrary choice -- needs tuning
        self.covar = np.diag(np.append(pos_sigma, vel_sigma))   # create covariance matrix (matrix of certainties of measurements)

        self.last_time_changed = dt.now()
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
        self.state, self.covar = kalman.predict(x=self.state, P=self.covar, F=self.state_trans, Q=0)

    def update(self, pos, vel, pos_sigma=None, vel_sigma=None):
        """Update object position and filter
        Inputs:
            pos -- position of obejct (cartesian)
            vel -- veloicty of obejct (cartesian)
            pos_sigma -- uncretainty of position of obejct (cartesian)
            vel_sigma -- uncertainty of veloicty of obejct (cartesian)
        """
        measurement = np.append(pos, vel)
        if pos_sigma is None:
            pos_sigma = np.array([20, 20])     # arbitrary choice -- needs tuning
        if vel_sigma is None:
            vel_sigma = np.array([50, 50])     # arbitrary choice -- needs tuning
        measurement_covar = np.diag(np.append(pos_sigma, vel_sigma))

        self.state, self.covar = kalman.update(x=self.state, P=self.covar, z=measurement, R=measurement_covar, H=self.measurement_trans)
        

    def _update_trans_matrix(self):
        """Updates transition matrix for time delta since last prediction
        Side Effects:
            self.state_trans -- updates velocity coefficients in position equations
            self.last_time_changed -- updates last time changed to reflect that state has changed
        """
        self.delta_t = dt.now() - self.last_time_changed
        # update delta_t in state transition matrix
        self.state_trans[0, 3] = self.delta_t
        self.state_trans[1, 4] = self.delta_t
        self.last_time_changed = dt.now()
