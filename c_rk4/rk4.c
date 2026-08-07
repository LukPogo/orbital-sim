#include <math.h>
#include <stdio.h>

//idea jest następująca: piszę funkcję, która wykonuje jeden krok algorytmu rk4

void vector_derivative(double t, double* y, int size_y, double* v){
    for (int i = 0; i < size_y; i++){
        v[i] = y[i];
    }
}

void vector_derivative_test(double t, const double* y, int size_y, double* y_derivative){
    y_derivative[0] = y[1];
    y_derivative[1] = -y[0];
}

void rk4_step(double t, const double* y, int size_y, void (*state_derivative)(double t, const double* y, int size_y, double* v), double h, double* y_out){

    double k1[size_y];
    double k2[size_y];
    double k3[size_y];
    double k4[size_y];
    double y_temp[size_y];

    state_derivative(t, y, size_y, k1);

    for (int i = 0; i < size_y; i++){
        y_temp[i] = y[i] + k1[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k2);

    for (int i = 0; i < size_y; i++){
        y_temp[i] = y[i] + k2[i] * h / 2;
    }

    state_derivative(t + h / 2, y_temp, size_y, k3);

    for (int i = 0; i < size_y; i++){
        y_temp[i] = y[i] + k3[i] * h;
    }

    state_derivative(t + h, y_temp, size_y, k4);

    for (int i = 0; i < size_y; i++){
        y_out[i] = y[i] + h / 6 * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]);
    }
}

// double rk4_loop(double t, double y, double* (*state_derivative)(double t, double y), double h, double eps){

//     double max_iter = 1000;
//     double y_n = 0;

//     for (int iter = 0; iter < max_iter; iter++){
//         y_n = rk4_step(t, y, state_derivative, h);
//         t += h;
//         y += y_n;
//     } 

// }

double constant_derivative(double t, double y){
    (void)t;
    (void)y;
    return 2.0;
}

double simple_derivative(double t, double y){
    (void)t;
    return y;
}

int main(){
    double t = 0;
    double y0 = 1;
    double y1 = 0;

    int size_y = 2;
    double y[size_y];
    double y_out[size_y];
    y[0] = y0;
    y[1] = y1;

    rk4_step(t, y, size_y, vector_derivative_test, 0.01, y_out);

    for (int i = 0; i < size_y; i++){
        printf("Wyjście %d: %lf\n", i, y_out[i]);
    }

    return 0;
}