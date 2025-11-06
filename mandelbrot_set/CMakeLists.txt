cmake_minimum_required(VERSION 3.15)
project(circle_mask LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 CONFIG REQUIRED)  # pip install pybind11[global]

pybind11_add_module(circle_mask mandelbrotCalculation.cpp)
