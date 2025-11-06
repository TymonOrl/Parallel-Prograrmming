#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

namespace py = pybind11;


static inline uint8_t pixel_value(double za, double zb,
                                    double ca, double cb,
                                    uint it, uint max_iteration, 
                                    double inf_cap) {
    double za_next = za*za - zb*zb + ca;
    if(abs(za_next) > inf_cap){
        return static_cast<uint16_t>(it);
    } else if (it >= max_iteration){
        return 0u;
    }
    double zb_next = 2.0*za*zb + cb;


    return pixel_value(za_next, zb_next, ca, cb, it+1, max_iteration, inf_cap);
}

py::array_t<uint8_t> mandelbrotCalc(
    uint width, uint height,
    double a_min, double a_max,
    double b_min, double b_max,
    uint max_iteration, double inf_cap
) {
    // Allocating array
    auto output = py::array_t<uint8_t>({height, width});
    auto arr = output.mutable_unchecked<2>(); // Gives direct read/write access

    // Precompute steps
    // c = a + i * b
    const double da = (a_max - a_min) / (width  - 1);
    const double db = (b_max - b_min) / (height - 1);

    // Release Python’s Global Interpreter Lock (GIL) during compute
    py::gil_scoped_release release;

    for (int dh = 0; dh < height; ++dh) {
        const double b = b_min + dh * db;
        for (int dw = 0; dw < width; ++dw) {
            const double a = a_min + dw * da;
            arr(dh, dw) = pixel_value(0, 0, a, b, 0, max_iteration, inf_cap);
        }
    }

    return output;
}


// Making python function definition
PYBIND11_MODULE(mandelbrotCalc, m) {
    m.doc() = "Calculates iteration per each space in a grid";
    m.def("mandelbrotCalc", &mandelbrotCalc,
          py::arg("width"), py::arg("height"),
          py::arg("a_min"), py::arg("a_max"),
          py::arg("b_min"), py::arg("b_max"),
          py::arg("max_iteration"), py::arg("inf_cap"));
}