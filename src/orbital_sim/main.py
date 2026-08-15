import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from cffi import FFI

from .constants import R_EARTH, ORB_HEIGHT, VEL_ISS, G, M_EARTH, M_ISS
from .dynamics import state_dot


def rk4(
    state_0: np.ndarray,
    t0: float,
    h: float,
    steps: int,
    size_y: int,
    y_his: np.ndarray,
    t_his: np.ndarray,
):

    ffi = FFI()

    ffi.cdef("""
    struct OrbitalData {
        const double m1;
        const double m2;
        const double G;
    };
    """)

    ffi.cdef("""void two_body_wrapper(const double *y0, double t0, double h, int steps,
                      const struct OrbitalData *params, double *y_history,
                      double *t_history);""")

    lib = ffi.dlopen("build/libc_rk4.so")

    y0 = ffi.from_buffer("double[]", state_0)

    y_history = ffi.from_buffer("double[]", y_his)
    t_history = ffi.from_buffer("double[]", t_his)

    params = ffi.new(
        "struct OrbitalData *",
        {
            "m1": M_EARTH,
            "m2": M_ISS,
            "G": G,
        },
    )
    lib.two_body_wrapper(y0, t0, h, steps, params, y_history, t_history)

    trajectory = y_his.reshape(steps + 1, size_y)

    # def main():
    #     state_0 = np.array([0, 0, 0, 0, 0, 0, R_EARTH + ORB_HEIGHT, 0, 0, 0, VEL_ISS, 0])
    #     t_start = 0
    #     t_end = 5800

    #     t_span = [t_start, t_end]
    #     t_eval = np.linspace(t_start, t_end, 10800)

    #     sol = solve_ivp(state_dot, t_span, state_0, t_eval=t_eval, method="DOP853")
    #     print(sol.success)
    #     print(sol.message)

    #     plt.plot(sol.y[6], sol.y[7])
    #     plt.axis("equal")
    #     plt.show()

    for step in range(steps + 1):
        start = step * size_y

        print("t =", t_history[step])
        print([y_history[start + i] for i in range(size_y)])


def main():
    state_0 = np.array(
        [0, 0, 0, 0, 0, 0, R_EARTH + ORB_HEIGHT, 0, 0, 0, VEL_ISS, 0], dtype=np.float64
    )
    steps = 2
    t0 = 0
    h = 0.01
    size_y = 12
    y_history = np.empty(size_y * (steps + 1))
    t_history = np.empty(steps + 1)

    rk4(state_0, t0, h, steps, size_y, y_history, t_history)


if __name__ == "__main__":
    main()
