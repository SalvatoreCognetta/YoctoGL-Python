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


// -----------------------------------------------------------------------------
// YOCTO-PATHTRACE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_pathtrace, m) {

  py::class_<vec2i>(m, "vec2i")
    .def(py::init<>())
    .def_readwrite("x", &vec2i::x)
    .def_readwrite("y", &vec2i::y);

  py::enum_<ptr::shader_type>(m, "shader_type")
    .value("naive", ptr::shader_type::naive)
    .value("path", ptr::shader_type::path)
    .value("eyelight", ptr::shader_type::eyelight)
    .value("normal", ptr::shader_type::normal)
    .export_values();

  py::object default_seed = py::cast(ptr::default_seed);
  m.attr("default_seed")  = default_seed;

  py::class_<ptr::trace_params>(m, "trace_params")
    .def(py::init<int, ptr::shader_type, int, int, float, uint64_t, bool, int>(), 
        py::arg("resolution") = 720,
        py::arg("shader") = ptr::shader_type::path,
        py::arg("samples") = 512,
        py::arg("bounces") = 8,
        py::arg("clamp") = 100,
        py::arg("seed") = default_seed,
        py::arg("noparallel") = false,
        py::arg("pratio") = 8
      )
    .def_readwrite("resolution", &ptr::trace_params::resolution)
    .def_readwrite("shader", &ptr::trace_params::shader)
    .def_readwrite("samples", &ptr::trace_params::samples)
    .def_readwrite("bounces", &ptr::trace_params::bounces)
    .def_readwrite("clamp", &ptr::trace_params::clamp)
    .def_readwrite("seed", &ptr::trace_params::seed)
    .def_readwrite("noparallel", &ptr::trace_params::noparallel)
    .def_readwrite("pratio", &ptr::trace_params::pratio);
  

  const py::object shader_names = py::cast(ptr::shader_names);
  m.attr("shader_names") = shader_names;

}

// -----------------------------------------------------------------------------
// YOCTO COMMONIO
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_commonio, m) {

  py::class_<cli::cli_state>(m, "cli_state")
    .def(py::init<std::string, std::string, std::vector<cli::cmdline_option>, std::string, std::string, bool>(), 
        py::arg("name") = "",
        py::arg("usage") = "",
        py::arg("options") = std::vector<cli::cmdline_option>{},
        py::arg("usage_options") = "",
        py::arg("usage_arguments") = "",
        py::arg("help") = false
      )
    .def_readwrite("name", &cli::cli_state::name)
    .def_readwrite("usage", &cli::cli_state::usage)
    .def_readwrite("options", &cli::cli_state::options)
    .def_readwrite("usage_options", &cli::cli_state::usage_options)
    .def_readwrite("usage_arguments", &cli::cli_state::usage_arguments)
    .def_readwrite("help", &cli::cli_state::help);

  m.def("make_cli", &cli::make_cli, "initialize a command line parser",
        py::arg("cmd"), py::arg("usage"));

  // https://github.com/pybind/pybind11/issues/1153 
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        std::string&, const std::string&, bool))&cli::add_option);
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        int&, const std::string&, bool))&cli::add_option);
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        float&, const std::string&, bool))&cli::add_option);
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        bool&, const std::string&, bool))&cli::add_option);
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        std::vector<std::string>&, const std::string&, bool))&cli::add_option);
  m.def("add_option", (void (*)(cli::cli_state&, const std::string&,
        int&, const std::string&, const std::vector<std::string>&, bool))&cli::add_option);
  
  // m.def("parse_cli", (void (*)(cli::cli_state&, int, const char**))&cli::parse_cli);
  // m.def("parse_cli", py::overload_cast<cli::cli_state&, int, const char**>(&cli::parse_cli));
  // https://stackoverflow.com/questions/49195418/pybind11-binding-a-function-that-uses-double-pointers
  m.def("parse_cli", [](cli::cli_state& cli, std::vector<std::string> argv) {
    std::vector<const char *> cstrs;
    // cstrs.reserve(argv.size()-1);
    for (auto &s : argv) cstrs.push_back((char *)(s.c_str()));
    // Delete the first element which is " ./apps/yscenetrace/yscentrace.py"
    // cstrs.erase(cstrs.begin());
    return cli::parse_cli(cli, cstrs.size(), cstrs.data());
  });

  m.def("print_progress", &cli::print_progress, py::arg("message"), py::arg("current"), py::arg("total"));
  m.def("print_fatal", &cli::print_fatal, py::arg("msg"));


}


// -----------------------------------------------------------------------------
// YOCTO SCENEIO
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_sceneio, m) {

  py::class_<sio::model>(m, "model")
    .def(py::init<std::vector<sio::camera*>,
                  std::vector<sio::object*>,
                  std::vector<sio::environment*>,
                  std::vector<sio::shape*>,
                  std::vector<sio::subdiv*>,
                  std::vector<sio::texture*>,
                  std::vector<sio::material*>,
                  std::vector<sio::instance*>,
                  std::string,
                  std::string>(), 
          py::arg("cameras") = std::vector<sio::camera*>{},
          py::arg("objects") = std::vector<sio::object*>{},
          py::arg("environments") = std::vector<sio::environment*>{},
          py::arg("shapes") = std::vector<sio::shape*>{},
          py::arg("subdivs") = std::vector<sio::subdiv*>{},
          py::arg("textures") = std::vector<sio::texture*>{},
          py::arg("materials") = std::vector<sio::material*>{},
          py::arg("instances") = std::vector<sio::instance*>{},
          py::arg("name") = "",
          py::arg("copyright") = ""
      )
    .def_readwrite("cameras", &sio::model::cameras)
    .def_readwrite("objects", &sio::model::objects)
    .def_readwrite("environments", &sio::model::environments)
    .def_readwrite("subdivs", &sio::model::subdivs)
    .def_readwrite("textures", &sio::model::subdivs)
    .def_readwrite("materials", &sio::model::materials)
    .def_readwrite("instances", &sio::model::instances)
    .def_readwrite("name", &sio::model::name)
    .def_readwrite("copyright", &sio::model::copyright)
    .def("get", [](){
      return std::make_unique<sio::model>().get();
    });

  m.def("load_scene", &sio::load_scene, py::arg("filename"), py::arg("scene"), py::arg("error"),
      py::arg("progress_cb"), py::arg("noparallel")); 
  m.def("make_cornellbox", &sio::make_cornellbox);

}


// -----------------------------------------------------------------------------
// YOCTO TRACE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_trace, m) {

  // const py::object coat_ior = py::cast(trace::coat_ior);
  // m.attr("coat_ior") = coat_ior; 

  // m.def("eval_normal", &trace::eval_normal);

}
  
}  // namespace yocto::extension