import numpy as np
from scipy.integrate import solve_ivp

from .dynamics import state_dot
from .c_rk4 import rk4
from .storage import h5_save_time_traj, initialize_h5_file
from .nasa_api import get_nasa_data


def generate_data():
    nasa_data = get_nasa_data()

    earth_state = np.zeros(6, dtype=np.float64)
    nasa_time, iss_state = nasa_data
    nasa_traj = iss_state
    earth_traj = np.zeros_like(nasa_traj)
    nasa_full_traj = np.concatenate((earth_traj, nasa_traj), axis=1)

    state_0 = np.concatenate((earth_state, iss_state[0, :]))

    t0 = 0
    tk = 864000
    h = 1
    steps = int((tk - t0) / h)
    t_span = [t0, tk]
    t_eval = t0 + h * np.arange(steps + 1)

    time, trajectory = rk4(state_0, t0, h, steps)
    sol = solve_ivp(
        state_dot,
        t_span,
        state_0,
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-13,
        atol=1e-15,
    )

    print("Generating data finished...")
    # Blok sprawdzający poprawność mojej wyprowadzonej metody
    initialize_h5_file("data.hdf5")
    h5_save_time_traj("data.hdf5", "rk4", time, trajectory)
    h5_save_time_traj("data.hdf5", "reference", sol.t, sol.y.T)
    h5_save_time_traj("data.hdf5", "nasa", nasa_time, nasa_full_traj)

    print("Saving data finished...")
