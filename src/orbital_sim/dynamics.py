import numpy as np

from .constants import G, M_EARTH, M_ISS

def state_dot(t: float, state: np.ndarray):
    #state comes as state = [x1, y1, z1, xdot1, ydot1, zdot1, x2, y2, z2, xdot2, ydot2, zdot2]
    x1 = state[0]
    y1 = state[1]
    z1 = state[2]

    x2 = state[6]
    y2 = state[7]
    z2 = state[8]

    velocities1 = state[3:6]
    velocities2 = state[9:12]

    #r vector is vector from the Earth (r1) to the satelite (r2)
    r = np.array([x2 - x1, y2 - y1, z2 - z1])
    r3 = np.power(np.dot(r, r), 3/2)

    acceleration1 = G*M_ISS/r3 * r
    acceleration2 = -G*M_EARTH/r3 * r

    dot_state = np.concatenate([velocities1, acceleration1, velocities2, acceleration2])

    return dot_state
