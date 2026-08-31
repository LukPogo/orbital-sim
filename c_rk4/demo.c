int main() {
    double t = 0;
    double x2 = 6371e3 + 400e3;

    struct OrbitalData ei_params = {
        .m1 = 5.9722e24, .m2 = 4.5e5, .G = 6.67430151515e-11};

    int steps = 50000;
    int size_y = 12;

    double y[size_y];
    double y_history[size_y * (steps + 1)];
    double t_history[steps + 1];

    for (int i = 0; i < size_y; i++) {
        y[i] = 0;
    }

    y[6] = x2;
    y[10] = 7.66e3;

    // double y_derivative[size_y];
    // two_body_derivative(t, y, size_y, y_derivative, &ei_params);

    // printf("Wektor stanu: \n");
    // for (int i = 0; i < size_y; i++) {
    //     printf("Wartosc %d:\t%e\n", i, y_derivative[i]);
    // }

    rk4(t, y, size_y, two_body_derivative, 0.01, steps, y_history, t_history,
        &ei_params);

    for (int i = 0; i < size_y * (steps + 1); i++) {
        printf("Wyjście %d: %e\n", i % size_y, y_history[i]);
    }

    return 0;
}
