import numpy as np
from cffi import FFI

from .constants import R_EARTH, ORB_HEIGHT, VEL_ISS, G, M_EARTH, M_ISS


def rk4(
    state_0: np.ndarray,
    t0: float,
    h: float,
    steps: int,
):
    size_y = state_0.shape[0]

    y_his = np.empty(size_y * (steps + 1))
    t_his = np.empty(steps + 1)

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
    y_his = y_his.reshape(steps + 1, size_y)

    return t_his, y_his
