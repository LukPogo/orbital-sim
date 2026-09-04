import numpy as np


def error_values(ref_traj: np.ndarray, traj: np.ndarray):
    ref_r = ref_traj[:, 6:9] - ref_traj[:, 0:3]
    traj_r = traj[:, 6:9] - traj[:, 0:3]

    r_error = np.linalg.norm(ref_r - traj_r, axis=1)

    ref_v = ref_traj[:, 9:12] - ref_traj[:, 3:6]
    traj_v = traj[:, 9:12] - traj[:, 3:6]

    v_error = np.linalg.norm(ref_v - traj_v, axis=1)
    return r_error, v_error


def error_reduction(baseline_error: float, improved_error: float) -> float:
    return (1 - improved_error / baseline_error) * 100
