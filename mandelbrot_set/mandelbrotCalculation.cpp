#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;


uint8_t circle_value(double x, double y) {
    return (x*x + y*y < 1.0) ? 0 : 255;
}

py::array_t<uint8_t> circle_mask(
   int width, int height,
    double a_min, double a_max,
    double b_min, double b_max
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
            arr(dh, dw) = circle_value(a, b);
        }
    }

    return output;
}


// Making python function definition
PYBIND11_MODULE(circle_mask, m) {
    m.doc() = "Return 0/1 mask for unit circle over a grid";
    m.def("circle_mask", &circle_mask,
          py::arg("width"), py::arg("height"),
          py::arg("a_min"), py::arg("a_max"),
          py::arg("b_min"), py::arg("b_max"));
}