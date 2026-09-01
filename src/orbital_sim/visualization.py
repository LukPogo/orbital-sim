import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from .constants import R_EARTH


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


def animate_orbiting_object(
    earth_traj: np.ndarray, iss_traj: np.ndarray, time: np.ndarray
):
    rel = iss_traj[:, 0:3] - earth_traj[:, 0:3]
    fig, ax = plt.subplots()
    max_range = np.max(np.abs(rel[:, 0:2]))
    limit = 1.1 * max_range
    tytul = ax.set_title(f"Animacja ruchu ISS wokół Ziemi w chwili t = {time[0]}[s]")
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    earth = Circle((0, 0), R_EARTH, label="Ziemia", color="sienna", zorder=1)
    ax.add_patch(earth)
    # ax.scatter(0, 0, label="Ziemia", color="sienna")
    iss = ax.scatter(rel[0, 0], rel[0, 1], label="ISS", color="navy", zorder=3)
    iss_trail = ax.plot(
        rel[0, 0],
        rel[0, 1],
        label="Trajektoria ISS",
        linestyle="--",
        color="powderblue",
        zorder=2,
    )[0]
    ax.axis("equal")
    ax.legend(loc="upper right")

    def update(frame):
        x = rel[frame, 0]
        y = rel[frame, 1]
        xt = rel[: frame + 1, 0]
        yt = rel[: frame + 1, 1]
        iss.set_offsets([[x, y]])
        iss_trail.set_xdata(xt)
        iss_trail.set_ydata(yt)
        tytul.set_text(f"Animacja ruchu ISS wokół Ziemi w chwili t = {time[frame]}[s]")
        return iss, iss_trail

    ani = animation.FuncAnimation(
        fig=fig, func=update, frames=range(0, rel.shape[0], 20), interval=10
    )
    plt.show()
