//
// Implementation for Yocto/Extension.
//

//
// LICENSE:
//
// Copyright (c) 2020 -- 2020 Fabio Pellacini
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//

#include "yocto_extension.h"

#include <pybind11/pybind11.h>

#include <atomic>
#include <deque>
#include <future>
#include <memory>
#include <mutex>
using namespace std::string_literals;

// -----------------------------------------------------------------------------
// MATH FUNCTIONS
// -----------------------------------------------------------------------------
namespace yocto::extension {

// import math symbols for use
using math::abs;
using math::acos;
using math::atan2;
using math::clamp;
using math::cos;
using math::exp;
using math::flt_max;
using math::fmod;
using math::fresnel_conductor;
using math::fresnel_dielectric;
using math::identity3x3f;
using math::invalidb3f;
using math::log;
using math::make_rng;
using math::max;
using math::min;
using math::pif;
using math::pow;
using math::sample_discrete_cdf;
using math::sample_discrete_cdf_pdf;
using math::sample_uniform;
using math::sample_uniform_pdf;
using math::sin;
using math::sqrt;
using math::zero2f;
using math::zero2i;
using math::zero3f;
using math::zero3i;
using math::zero4f;
using math::zero4i;

}  // namespace yocto::extension

// -----------------------------------------------------------------------------
// IMPLEMENTATION FOR EXTENSION
// -----------------------------------------------------------------------------
namespace yocto::extension {
namespace py = pybind11;

PYBIND11_MODULE(py_yocto, m) {
  py::class_<vec2i>(m, "vec2i")
      .def(py::init<>())
      .def_readwrite("x", &vec2i::x)
      .def_readwrite("y", &vec2i::y);

  py::object default_seed = py::cast(pathtrace::default_seed);
  m.attr("default_seed")  = default_seed;

  py::class_<trace_params>(m, "trace_params")
      .def(py::init<int, int, int, int, int>(), 
          py::arg("resolution") = 720,
          py::arg("samples") = 512, 
          py::arg("bounces") = 8,
          py::arg("clamp") = 100,
          py::arg("seed") = default_seed)
      .def_readwrite("resolution", &trace_params::resolution)
      .def_readwrite("samples", &trace_params::samples)
      .def_readwrite("bounces", &trace_params::bounces)
      .def_readwrite("clamp", &trace_params::clamp)
      .def_readwrite("seed", &trace_params::seed);
}

}  // namespace yocto::extension
