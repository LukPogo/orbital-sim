import numpy as np
import argparse

from .data_generation import generate_data
from .storage import h5_load_time_traj
from .analysis import error_values
from .visualization import (
    plot_earth_center,
    plot_reference_comparison,
    animate_earth_iss_2d,
    animate_earth_iss_3d_comparison,
)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    if args.generate:
        print("Generating simulation data...")
        generate_data()
    else:
        print("Using existing simulation data...")

    rk4_time, rk4_traj = h5_load_time_traj("data.hdf5", "rk4")
    ref_time, ref_traj = h5_load_time_traj("data.hdf5", "reference")
    nasa_time, nasa_traj = h5_load_time_traj("data.hdf5", "nasa")

    print(error_values(ref_traj, rk4_traj))

    plot_earth_center(rk4_traj[:, 0:6], rk4_traj[:, 6:12])
    plot_reference_comparison(ref_traj, rk4_traj, ref_time)

    animate_earth_iss_2d(rk4_traj[:, 0:3], rk4_traj[:, 6:9], rk4_time)

    # Blok kodu odpowiedzialny za porównanie z danymi od NASA:
    mask = nasa_time <= rk4_time[-1]
    nasa_time = nasa_time[mask]
    nasa_traj = nasa_traj[mask]

    rk4_indices = nasa_time.astype(int)

    rk4_at_nasa_times = rk4_traj[rk4_indices, :]

    plot_reference_comparison(nasa_traj, rk4_at_nasa_times, nasa_time)

    animate_earth_iss_3d_comparison(nasa_traj, rk4_at_nasa_times, nasa_time)


if __name__ == "__main__":
    main()
