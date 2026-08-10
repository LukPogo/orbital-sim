#include <math.h>
#include <stdio.h>

struct OrbitalData {
    const double m1;
    const double m2;
    const double G;
};

void vector_derivative(double t, double *y, int size_y, double *v) {
    for (int i = 0; i < size_y; i++) {
        v[i] = y[i];
    }
}

void two_body_derivative(double t, const double *y, int size_y,
                         double *y_derivative, void *params);

void vector_derivative_test(double t, const double *y, int size_y,
                            double *y_derivative) {
    y_derivative[0] = y[1];
    y_derivative[1] = -y[0];
}

void rk4_step(double t, const double *y, int size_y,
              void (*state_derivative)(double t, const double *y, int size_y,
                                       double *v, void *params),
              double h, double *y_out, void *params) {

    double k1[size_y];
    double k2[size_y];
    double k3[size_y];
    double k4[size_y];
    double y_temp[size_y];

    state_derivative(t, y, size_y, k1);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k1[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k2);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k2[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k3);

    for (int i = 0; i < size_y; i++) {
        y_temp[i] = y[i] + k3[i] * h;
    }

    state_derivative(t + h, y_temp, size_y, k4);

    for (int i = 0; i < size_y; i++) {
        y_out[i] = y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]);
    }
}

void refresh_vector(double *y, double *x, int size_y) {
    for (int i = 0; i < size_y; i++) {
        y[i] = x[i];
    }
}

void rk4(double t0, double *y0, int size_y,
         void (*state_derivative)(double t, const double *y, int size_y,
                                  double *v, void *params),
         double h, int steps, double *y_history, double *t_history,
         void *params) {

    double y[size_y];
    double t = t0;
    double y_out[size_y];
    refresh_vector(y, y0, size_y);
    refresh_vector(y_history, y, size_y);
    t_history[0] = t;

    for (int step = 0; step < steps; step++) {
        rk4_step(t, y, size_y, state_derivative, h, y_out);
        t = t + h;
        refresh_vector(y, y_out, size_y);
        for (int i = 0; i < size_y; i++) {
            y_history[i + size_y * (step + 1)] = y_out[i];
        }
        t_history[(step + 1)] = t;
    }

    refresh_vector(y0, y, size_y);
}

int main() {
    double t = 0;
    double y0 = 1;
    double y1 = 1;

    int steps = 2;
    int size_y = 2;
    double y[size_y];
    double y_history[size_y * (steps + 1)];
    y[0] = y0;
    y[1] = y1;

    rk4(t, y, size_y, vector_derivative_test, 0.01, steps, y_history);

    for (int i = 0; i < size_y * (steps + 1); i++) {
        printf("Wyjście %d: %lf\n", i % size_y, y_history[i]);
    }

    return 0;
}
