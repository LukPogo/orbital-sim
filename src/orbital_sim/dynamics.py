import numpy as np

from .constants import M_EARTH, MU_EARTH, M_ISS, J2_EARTH, R_EARTH_J2


def state_dot(t: float, state: np.ndarray, use_J2: bool):
    # state comes as state = [x1, y1, z1, xdot1, ydot1, zdot1, x2, y2, z2, xdot2, ydot2, zdot2]
    x1 = state[0]
    y1 = state[1]
    z1 = state[2]

    x2 = state[6]
    y2 = state[7]
    z2 = state[8]

    velocities1 = state[3:6]
    velocities2 = state[9:12]

    # r vector is vector from the Earth (r1) to the satelite (r2)
    r = np.array([x2 - x1, y2 - y1, z2 - z1])
    r2 = np.dot(r, r)
    r_norm = np.sqrt(r2)
    r3 = r2 * r_norm
    r5 = r3 * r2

    acceleration1 = (MU_EARTH / M_EARTH) * M_ISS / r3 * r
    acceleration2 = -MU_EARTH / r3 * r

    # Składowa harmoniczna J2 z rozwiązania równania Laplace'a
    # aJ2x =  3miJ2R_EARTH^2/ 2*r^5 * x * (5z^2/r^2 -1)
    if use_J2:
        bJ2 = 3 * MU_EARTH * J2_EARTH * R_EARTH_J2**2 / (2 * r5)
        aJ2 = bJ2 * np.array(
            [
                r[0] * (5 * r[2] ** 2 / r2 - 1),
                r[1] * (5 * r[2] ** 2 / r2 - 1),
                r[2] * (5 * r[2] ** 2 / r2 - 3),
            ]
        )

        acceleration1 -= aJ2 * (M_ISS / M_EARTH)
        acceleration2 += aJ2

    dot_state = np.concatenate([velocities1, acceleration1, velocities2, acceleration2])

    return dot_state
