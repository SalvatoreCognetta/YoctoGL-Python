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

PYBIND11_MODULE(py_pathtrace, m) {
  
  const py::object shader_names = py::cast(pathtrace::shader_names);
  m.attr("shader_names") = shader_names;  

  py::class_<vec2i>(m, "vec2i")
    .def(py::init<>())
    .def_readwrite("x", &vec2i::x)
    .def_readwrite("y", &vec2i::y);

  py::enum_<pathtrace::shader_type>(m, "shader_type")
    .value("naive", pathtrace::shader_type::naive)
    .value("path", pathtrace::shader_type::path)
    .value("eyelight", pathtrace::shader_type::eyelight)
    .value("normal", pathtrace::shader_type::normal)
    .export_values();

  py::object default_seed = py::cast(pathtrace::default_seed);
  m.attr("default_seed")  = default_seed;

  py::class_<pathtrace::trace_params>(m, "trace_params")
    .def(py::init<int, pathtrace::shader_type, int, int, float, uint64_t, bool, int>(), 
        py::arg("resolution") = 720,
        py::arg("shader") = pathtrace::shader_type::path,
        py::arg("samples") = 512,
        py::arg("bounces") = 8,
        py::arg("clamp") = 100,
        py::arg("seed") = default_seed,
        py::arg("noparallel") = false,
        py::arg("pratio") = 8
      )
    .def_readwrite("resolution", &pathtrace::trace_params::resolution)
    .def_readwrite("shader", &pathtrace::trace_params::shader)
    .def_readwrite("samples", &pathtrace::trace_params::samples)
    .def_readwrite("bounces", &pathtrace::trace_params::bounces)
    .def_readwrite("clamp", &pathtrace::trace_params::clamp)
    .def_readwrite("seed", &pathtrace::trace_params::seed)
    .def_readwrite("noparallel", &pathtrace::trace_params::noparallel)
    .def_readwrite("pratio", &pathtrace::trace_params::pratio);
  

}


PYBIND11_MODULE(py_commonio, m) {

  py::class_<commonio::cli_state>(m, "cli_state")
    .def(py::init<std::string, std::string, std::vector<commonio::cmdline_option>, std::string, std::string, bool>(), 
        py::arg("name") = "",
        py::arg("usage") = "",
        py::arg("options") = std::vector<commonio::cmdline_option>{}, //It should be = {}
        py::arg("usage_options") = "",
        py::arg("usage_arguments") = "",
        py::arg("help") = false
      )
    .def_readwrite("name", &commonio::cli_state::name)
    .def_readwrite("usage", &commonio::cli_state::usage)
    .def_readwrite("options", &commonio::cli_state::options)
    .def_readwrite("usage_options", &commonio::cli_state::usage_options)
    .def_readwrite("usage_arguments", &commonio::cli_state::usage_arguments)
    .def_readwrite("help", &commonio::cli_state::help);

  m.def("make_cli", &commonio::make_cli, "initialize a command line parser",
        py::arg("cmd"), py::arg("usage"));
  
  m.def("add_option", (void (*)(commonio::cli_state&, const std::string&,
        std::string&, const std::string&, bool))&commonio::add_option);
  m.def("add_option", (void (*)(commonio::cli_state&, const std::string&,
        int&, const std::string&, bool))&commonio::add_option);


  m.def("add_option", (void (*)(commonio::cli_state&, const std::string&,
        std::vector<std::string>&, const std::string&, bool))&commonio::add_option);

}


PYBIND11_MODULE(py_sceneio, m) {

   m.def("load_scene", &ysceneio::load_scene, py::arg("filename"), py::arg("scene"), py::arg("error"),
        py::arg("progress_cb"), py::arg("noparallel")); 

}
  
}  // namespace yocto::extension