# Very good implementation resource
# https://share.cocalc.com/share/7557a5ac1c870f1ec8f01271959b16b49df9d087/Kalman-and-Bayesian-Filters-in-Python/11-Extended-Kalman-Filters.ipynb?viewer=share

import scipy
from sympy import symbols, tan, sin, cos, Matrix

def define_model():
    a, x, y, v, w, theta, time = symbols('a, x, y, v, w, theta, t')
    d = v * time
    beta = (d / w) * tan(a)
    R = w / tan(a)

    fxu = Matrix([[x - R * sin(theta) + R * sin(theta + beta)],
                  [y + R * cos(theta) - R * cos(theta + beta)],
                  [theta + beta]])

    return fxu.jacobian(Matrix([x, y, theta]))
