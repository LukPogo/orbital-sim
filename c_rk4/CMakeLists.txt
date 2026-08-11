cmake_minimum_required(VERSION 3.20)
project(c_rk4 LANGUAGES C)

add_library(c_rk4 SHARED rk4.c)
target_link_libraries(c_rk4 PRIVATE m)