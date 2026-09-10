#include <math.h>
#include <stdbool.h>

struct OrbitalData {
    const double m1;
    const double m2;
    const double G;
    const double r_earth_J2;
    const double J2;
    const bool use_J2;
};

void two_body_derivative(double t, const double *y, int size_y,
                         double *y_derivative, const void *params) {
    const struct OrbitalData *data = params;
    double m1 = data->m1;
    double m2 = data->m2;
    double G = data->G;
    double r_earth_J2 = data->r_earth_J2;
    double J2 = data->J2;
    bool use_J2 = data->use_J2;
    double r[3];
    double r3;
    double a1[3];
    double a2[3];

    (void)size_y;
    (void)t;

    double x1, x2, y1, y2, z1, z2;

    x1 = y[0];
    y1 = y[1];
    z1 = y[2];

    x2 = y[6];
    y2 = y[7];
    z2 = y[8];

    r[0] = x2 - x1;
    r[1] = y2 - y1;
    r[2] = z2 - z1;

    double r_abs = sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2]);

    r3 = pow(r_abs, 3);

    a1[0] = G * m2 / r3 * r[0];
    a1[1] = G * m2 / r3 * r[1];
    a1[2] = G * m2 / r3 * r[2];

    a2[0] = -G * m1 / r3 * r[0];
    a2[1] = -G * m1 / r3 * r[1];
    a2[2] = -G * m1 / r3 * r[2];

    if (use_J2) {
        double aJ2[3];
        double r2 = pow(r_abs, 2);
        double r5 = pow(r_abs, 5);
        double bJ2 = 3 * m1 * G * J2 * pow(r_earth_J2, 2) / (2 * r5);
        aJ2[0] = bJ2 * r[0] * (5 * pow(r[2], 2) / r2 - 1);
        aJ2[1] = bJ2 * r[1] * (5 * pow(r[2], 2) / r2 - 1);
        aJ2[2] = bJ2 * r[2] * (5 * pow(r[2], 2) / r2 - 3);

        a1[0] = a1[0] - aJ2[0] * (m2 / m1);
        a1[1] = a1[1] - aJ2[1] * (m2 / m1);
        a1[2] = a1[2] - aJ2[2] * (m2 / m1);

        a2[0] = a2[0] + aJ2[0];
        a2[1] = a2[1] + aJ2[1];
        a2[2] = a2[2] + aJ2[2];
    }

    y_derivative[0] = y[3];
    y_derivative[1] = y[4];
    y_derivative[2] = y[5];

    y_derivative[6] = y[9];
    y_derivative[7] = y[10];
    y_derivative[8] = y[11];

    y_derivative[3] = a1[0];
    y_derivative[4] = a1[1];
    y_derivative[5] = a1[2];

    y_derivative[9] = a2[0];
    y_derivative[10] = a2[1];
    y_derivative[11] = a2[2];
}

void rk4_step(double t, const double *y, int size_y,
              void (*state_derivative)(double t, const double *y, int size_y,
                                       double *v, const void *params),
              double h, double *y_out, const void *params) {

    double k1[size_y];
    double k2[size_y];
    double k3[size_y];
    double k4[size_y];
    double y_temp[size_y];

    state_derivative(t, y, size_y, k1, params);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k1[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k2, params);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k2[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k3, params);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k3[i] * h;
    }

    state_derivative(t + h, y_temp, size_y, k4, params);

    for (int i = 0; i < size_y; i++) {
        y_out[i] = y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    }
}

void refresh_vector(double *y, const double *x, int size_y) {
    for (int i = 0; i < size_y; i++) {
        y[i] = x[i];
    }
}

void rk4(double t0, const double *y0, int size_y,
         void (*state_derivative)(double t, const double *y, int size_y,
                                  double *v, const void *params),
         double h, int steps, double *y_history, double *t_history,
         const void *params) {

    double y[size_y];
    double t = t0;
    double y_out[size_y];
    refresh_vector(y, y0, size_y);
    refresh_vector(y_history, y, size_y);
    t_history[0] = t;

    for (int step = 0; step < steps; step++) {
        rk4_step(t, y, size_y, state_derivative, h, y_out, params);
        t = t + h;
        refresh_vector(y, y_out, size_y);
        for (int i = 0; i < size_y; i++) {
            y_history[i + size_y * (step + 1)] = y_out[i];
        }
        t_history[(step + 1)] = t;
    }
}

void two_body_wrapper(const double *y0, double t0, double h, int steps,
                      const struct OrbitalData *params, double *y_history,
                      double *t_history) {
    int size_y = 12;

    rk4(t0, y0, size_y, two_body_derivative, h, steps, y_history, t_history,
        params);
}
