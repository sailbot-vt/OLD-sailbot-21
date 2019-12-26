from filterpy.kalman import ExtendedKalmanFilter as EKF
from numpy import dot, array, sqrt
import sympy

#Needs filterpy and sympy packages

class RobotEKF(EKF):
    def __init__(self, dt, wheelbase, sigma_vel, sigma_steer):
        EKF.__init__(self, 3, 2, 2)
        self.dt = dt
        self.wheelbase = wheelbase
        self.sigma_vel = sigma_vel
        self.sigma_steer = sigma_steer

        a, x, y, v, w, theta, time = symbols('a, x, y, v, w, theta, t')
        d = v * time
        beta = (d / w) * sympy.tan(a)
        r = w / sympy.tan(a)

        self.fxu = Matrix([[x - r * sympy.sin(theta) + r * sympy.sin(theta + beta)],
                           [y + r * sympy.cos(theta) - r * sympy.cos(theta + beta)],
                           [theta + beta]])

        self.F_j = self.fxu.jacobian(Matrix([x, y, theta]))
        self.V_j = self.fxu.jacobian(Matrix([v, a]))

        # save dictionary and it's variables for later use
        self.subs = {x: 0, y: 0, v: 0, a: 0, time: dt, w: wheelbase, theta: 0}
        self.x_x, self.x_y, self.v, self.a, self.theta = x, y, v, a, theta

    def predict(self, u=0):
        self.x = self.move(self.x, u, self.dt)

        self.subs[self.theta] = self.x[2, 0]
        self.subs[self.v] = u[0]
        self.subs[self.a] = u[1]

        F = array(self.F_j.evalf(subs=self.subs)).astype(float)
        V = array(self.V_j.evalf(subs=self.subs)).astype(float)

        # covariance of motion noise in control space
        M = array([[self.sigma_vel * u[0] ** 2, 0], [0, self.sigma_steer ** 2]])

        self.P = dot(F, self.P).dot(F.T) + dot(V, M).dot(V.T)

    def move(self, x, u, dt):
        h = x[2, 0]
        v = u[0]
        steering_angle = u[1]

        dist = v * dt

        if abs(steering_angle) < 0.0001:
            # approximate straight line with huge radius
            r = 1.e-30
        b = dist / self.wheelbase * tan(steering_angle)
        r = self.wheelbase / tan(steering_angle)  # radius
        sinh = sin(h)
        sinhb = sin(h + b)
        cosh = cos(h)
        coshb = cos(h + b)
        return x + array([[-r * sinh + r * sinhb],
                          [r * cosh - r * coshb],
                          [b]])