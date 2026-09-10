import numpy as np
import argparse

from .data_generation import generate_data
from .storage import h5_load_time_traj
from .analysis import error_values, error_reduction
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
    ref_time_J2, ref_traj_J2 = h5_load_time_traj("data.hdf5", "reference_J2")
    rk4_time_J2, rk4_traj_J2 = h5_load_time_traj("data.hdf5", "rk4_J2")
    nasa_time, nasa_traj = h5_load_time_traj("data.hdf5", "nasa")

    r_error_ref, v_error_ref = error_values(ref_traj, rk4_traj)

    print("\nRK4 vs DOP853 reference:")
    print(f"Final position error: {r_error_ref[-1]:.3f} m")
    print(f"Final velocity error: {v_error_ref[-1]:.6f} m/s")

    plot_earth_center(rk4_traj[:, 0:6], rk4_traj[:, 6:12])
    plot_reference_comparison(
        ref_traj,
        rk4_traj,
        ref_time,
        "docs/images/rk4_reference_error.png",
    )

    animate_earth_iss_2d(rk4_traj[:, 0:3], rk4_traj[:, 6:9], rk4_time)

    # Blok kodu odpowiedzialny za porównanie z danymi od NASA:
    mask = nasa_time <= rk4_time[-1]
    nasa_time = nasa_time[mask]
    nasa_traj = nasa_traj[mask]

    rk4_indices = np.searchsorted(rk4_time, nasa_time)

    if not np.allclose(rk4_time[rk4_indices], nasa_time):
        raise ValueError("NASA timestamps do not align with RK4 timestamps")

    rk4_at_nasa_times = rk4_traj[rk4_indices]
    rk4_at_nasa_times_J2 = rk4_traj_J2[rk4_indices]

    plot_reference_comparison(
        nasa_traj,
        rk4_at_nasa_times_J2,
        nasa_time,
        "docs/images/nasa_rk4_comparison.png",
    )

    animate_earth_iss_3d_comparison(nasa_traj, rk4_at_nasa_times_J2, nasa_time)

    r_error, v_error = error_values(nasa_traj, rk4_at_nasa_times)
    r_error_J2, v_error_J2 = error_values(nasa_traj, rk4_at_nasa_times_J2)

    position_improvement = error_reduction(r_error[-1], r_error_J2[-1])

    velocity_improvement = error_reduction(v_error[-1], v_error_J2[-1])

    print("\nComparison against NASA OEM:")
    print(f"Final position error without J2: {r_error[-1]:.3f} m")
    print(f"Final position error with J2:    {r_error_J2[-1]:.3f} m")
    print(f"Position error reduction:        {position_improvement:.2f} %")

    print(f"Final velocity error without J2: {v_error[-1]:.6f} m/s")
    print(f"Final velocity error with J2:    {v_error_J2[-1]:.6f} m/s")
    print(f"Velocity error reduction:        {velocity_improvement:.2f} %")


if __name__ == "__main__":
    main()
