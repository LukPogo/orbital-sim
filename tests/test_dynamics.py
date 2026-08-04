import numpy as np
from orbital_sim.dynamics import state_dot
from orbital_sim.constants import M_EARTH, M_ISS

def test_position_derivatives_equal_velocities():
    state = np.array([
        0, 0, 0,
        100, 20, 30,
        1000, 0, 0,
        -7, -6, -9
    ])
    derivative = state_dot(0.0, state)
    np.testing.assert_allclose(derivative[0:3], state[3:6])
    np.testing.assert_allclose(derivative[6:9], state[9:12])

def test_acceleration_point_towards_each_other():
    state = np.array([
        0, 0, 0,
        0, 0, 0,
        1000, 0, 0,
        0, 0, 0
    ])
    derivative = state_dot(0.0, state)

    assert derivative[3] > 0
    assert derivative[9] < 0
    np.testing.assert_allclose(derivative[4:6], [0., 0.])
    np.testing.assert_allclose(derivative[10:12], [0., 0.])

def test_internal_gravitational_forces_are_equal_and_opposite():
    state = np.array([
        0, 0, 0,
        0, 0, 0,
        1000, 2000, -500,
        0, 0, 0
    ])
    derivative = state_dot(0.0, state)
    acceleration_earth = derivative[3:6]
    acceleration_iss = derivative[9:12]

    force_earth = M_EARTH*acceleration_earth
    force_iss = M_ISS*acceleration_iss

    np.testing.assert_allclose(force_earth, -force_iss, rtol=1e-12)