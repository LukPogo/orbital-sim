import numpy as np
import matplotlib.pyplot as plt


def plot_earth_center(earth_traj: np.ndarray, iss_traj: np.ndarray):
    rel = iss_traj[:, 0:3] - earth_traj[:, 0:3]
    fig, ax = plt.subplots()
    ax.set_title("Earth-centered ISS trajectory plot")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.axis("equal")
    ax.plot(rel[:, 0], rel[:, 1], label="Trajektoria ISS")
    ax.scatter(0, 0, label="Ziemia")
    ax.legend(loc="upper right")
    plt.show()


def plot_reference_comparison(
    ref_traj: np.ndarray, rk4_traj: np.ndarray, time: np.ndarray
):
    r_ref_relative = ref_traj[:, 6:9] - ref_traj[:, 0:3]
    r_rk4_relative = rk4_traj[:, 6:9] - rk4_traj[:, 0:3]
    delta_r = r_ref_relative - r_rk4_relative
    delta_r = np.linalg.norm(delta_r, axis=1)
    print(delta_r[-1])
    fig, ax = plt.subplots()
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel(r"$\|\Delta \mathbf{r}(t)\|$ [m]")
    ax.set_title(
        "Błąd pozycji ISS względem rozwiązania referencyjnego (Earth-centered)"
    )
    ax.plot(time, delta_r)
    plt.show()
