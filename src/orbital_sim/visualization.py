import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import cast
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Line3D, Path3DCollection
from .constants import R_EARTH

plt.rcParams["figure.figsize"] = (12, 8)


def plot_earth_center(earth_traj: np.ndarray, iss_traj: np.ndarray):
    rel = iss_traj[:, 0:3] - earth_traj[:, 0:3]
    fig, ax = plt.subplots()
    ax.set_title("Earth-centered ISS trajectory plot")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.axis("equal")
    ax.plot(rel[:, 0], rel[:, 1], label="ISS trajectory")
    earth = Circle((0, 0), R_EARTH, label="Earth", color="sienna")
    ax.add_patch(earth)
    ax.legend(loc="upper right")
    plt.show()


def plot_reference_comparison(
    ref_traj: np.ndarray, rk4_traj: np.ndarray, time: np.ndarray
):
    r_ref_relative = ref_traj[:, 6:9] - ref_traj[:, 0:3]
    r_rk4_relative = rk4_traj[:, 6:9] - rk4_traj[:, 0:3]
    delta_r = r_ref_relative - r_rk4_relative
    delta_r = np.linalg.norm(delta_r, axis=1)
    fig, ax = plt.subplots()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(r"$\|\Delta \mathbf{r}(t)\|$ [m]")
    ax.set_title("ISS position error against reference (Earth-centered)")
    ax.plot(time, delta_r)
    plt.show()


def animate_earth_iss_2d(
    earth_traj: np.ndarray, iss_traj: np.ndarray, time: np.ndarray
):
    rel = iss_traj[:, 0:3] - earth_traj[:, 0:3]
    fig, ax = plt.subplots()
    max_range = np.max(np.abs(rel[:, 0:2]))
    limit = 1.1 * max_range
    title = ax.set_title(f"ISS around Earth in t = {time[0]/3600:.1f} h")
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    earth = Circle((0, 0), R_EARTH, label="Earth", color="sienna", zorder=1)
    ax.add_patch(earth)
    # ax.scatter(0, 0, label="Ziemia", color="sienna")
    iss = ax.scatter(rel[0, 0], rel[0, 1], label="ISS", color="navy", zorder=3)
    iss_trail = ax.plot(
        rel[0, 0],
        rel[0, 1],
        label="Past ISS trajectory",
        linestyle="--",
        color="powderblue",
        zorder=2,
    )[0]
    ax.axis("equal")
    ax.legend(loc="upper right")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")

    def update(frame):
        x = rel[frame, 0]
        y = rel[frame, 1]
        xt = rel[: frame + 1, 0]
        yt = rel[: frame + 1, 1]
        iss.set_offsets([[x, y]])
        iss_trail.set_xdata(xt)
        iss_trail.set_ydata(yt)
        title.set_text(f"ISS around Earth in t = {time[frame]/3600:.1f} h")
        return iss, iss_trail

    ani = animation.FuncAnimation(
        fig=fig, func=update, frames=range(0, rel.shape[0], 20), interval=10
    )
    plt.show()


def animate_earth_iss_3d_comparison(
    nasa_traj: np.ndarray, rk4_traj: np.ndarray, nasa_time: np.ndarray
):
    nasa_rel = nasa_traj[:, 6:9] - nasa_traj[:, 0:3]
    rk4_rel = rk4_traj[:, 6:9] - rk4_traj[:, 0:3]

    ax = plt.figure().add_subplot(projection="3d", computed_zorder=False)
    max_range = max(np.max(np.abs(rk4_rel)), np.max(np.abs(nasa_rel)))
    limit = 1.1 * max_range
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("Z [m]")
    title = ax.set_title(f"RK4 vs NASA trajectory — t = {nasa_time[0]/3600:.1f} h")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=50)

    # Eearth sphere parametrization
    u = np.linspace(0, 2 * np.pi, 16)
    v = np.linspace(0, np.pi, 8)

    u, v = np.meshgrid(u, v)

    x = R_EARTH * np.sin(v) * np.cos(u)
    y = R_EARTH * np.sin(v) * np.sin(u)
    z = R_EARTH * np.cos(v)

    ax.plot_surface(x, y, z, color="sienna", label="Earth", alpha=0.7, zorder=1)

    nasa_plot = cast(
        Line3D,
        ax.plot3D(
            nasa_rel[0, 0],
            nasa_rel[0, 1],
            nasa_rel[0, 2],
            color="lime",
            linestyle="--",
            label="NASA past trajectory",
            zorder=2,
        )[0],
    )
    rk4_plot = cast(
        Line3D,
        ax.plot3D(
            rk4_rel[0, 0],
            rk4_rel[0, 1],
            rk4_rel[0, 2],
            color="navy",
            linestyle="--",
            label="RK4 past trajectory",
            zorder=3,
        )[0],
    )
    rk4_marker = cast(
        Path3DCollection,
        ax.scatter(
            rk4_rel[0, 0],
            rk4_rel[0, 1],
            rk4_rel[0, 2],
            color="navy",
            label="RK4 ISS",
            zorder=3,
        ),
    )
    nasa_marker = cast(
        Path3DCollection,
        ax.scatter(
            nasa_rel[0, 0],
            nasa_rel[0, 1],
            nasa_rel[0, 2],
            color="lime",
            label="NASA ISS",
            zorder=2,
        ),
    )
    ax.legend()

    def update(frame):
        nasa_plot.set_data_3d(
            nasa_rel[: frame + 1, 0], nasa_rel[: frame + 1, 1], nasa_rel[: frame + 1, 2]
        )
        rk4_plot.set_data_3d(
            rk4_rel[: frame + 1, 0], rk4_rel[: frame + 1, 1], rk4_rel[: frame + 1, 2]
        )
        rk4_marker.set_offsets([rk4_rel[frame, 0], rk4_rel[frame, 1]])
        rk4_marker.set_3d_properties(rk4_rel[frame, 2], zdir="z")

        nasa_marker.set_offsets([nasa_rel[frame, 0], nasa_rel[frame, 1]])
        nasa_marker.set_3d_properties(nasa_rel[frame, 2], zdir="z")

        title.set_text(f"RK4 vs NASA trajectory — t = {nasa_time[frame]/3600:.1f} h")

        return nasa_plot, rk4_plot, rk4_marker, nasa_marker

    ani = animation.FuncAnimation(
        fig=ax.figure, func=update, frames=range(0, nasa_time.shape[0], 1), interval=20
    )
    plt.show()
