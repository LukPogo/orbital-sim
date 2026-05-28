import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from .constants import R_EARTH, ORB_HEIGHT, VEL_ISS
from .dynamics import state_dot

def main():
    state_0 = np.array([0, 0, 0, 0, 0, 0, R_EARTH + ORB_HEIGHT, 0, 0, 0, VEL_ISS, 0])
    t_start = 0
    t_end = 5800

    t_span = [t_start, t_end]
    t_eval = np.linspace(t_start, t_end, 10800)

    sol = solve_ivp(state_dot, t_span, state_0, t_eval=t_eval, method='DOP853')
    print(sol.success)
    print(sol.message)

    plt.plot(sol.y[6], sol.y[7])
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()