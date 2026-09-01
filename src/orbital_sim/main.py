import numpy as np
from scipy.integrate import solve_ivp

from .constants import R_EARTH, ORB_HEIGHT, VEL_ISS, G, M_EARTH, M_ISS
from .dynamics import state_dot
from .c_rk4 import rk4
from .storage import h5_save_time_traj, h5_load_time_traj, initialize_h5_file
from .analysis import error_values
from .visualization import (
    plot_earth_center,
    plot_reference_comparison,
    animate_orbiting_object,
)
from .nasa_api import get_nasa_data


def main():
    nasa_data = get_nasa_data()

    earth_state = np.zeros(6, dtype=np.float64)
    iss_state = nasa_data[0, :]

    state_0 = np.concatenate((earth_state, iss_state))

    t0 = 0
    tk = 86400
    h = 2.5
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

    initialize_h5_file("data.hdf5")
    h5_save_time_traj("data.hdf5", "rk4", time, trajectory)
    h5_save_time_traj("data.hdf5", "reference", sol.t, sol.y.T)

    rk4_time, rk4_traj = h5_load_time_traj("data.hdf5", "rk4")
    ref_time, ref_traj = h5_load_time_traj("data.hdf5", "reference")

    print(error_values(ref_traj, rk4_traj))

    # plot_earth_center(rk4_traj[:, 0:6], rk4_traj[:, 6:12])
    # plot_reference_comparison(ref_traj, rk4_traj, ref_time)

    animate_orbiting_object(rk4_traj[:, 0:3], rk4_traj[:, 6:9], rk4_time)


if __name__ == "__main__":
    main()
