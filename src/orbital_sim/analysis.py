import numpy as np


def error_values(ref_traj: np.ndarray, traj: np.ndarray):
    error = ref_traj - traj
    r_error = np.linalg.norm(error[6:9], axis=0)
    v_error = np.linalg.norm(error[9:12], axis=0)
    return r_error, v_error
