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
// YOCTO-MATH
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_math, m) {

  // -----------------------------------------------------------------------------
  // VECTORS
  // -----------------------------------------------------------------------------
  py::class_<vec2f>(m, "vec2f")
    .def(py::init<float, float>(), py::arg("x") = 0, py::arg("y") = 0)
    .def_readwrite("x", &vec2f::x)
    .def_readwrite("y", &vec2f::y);

  py::class_<vec3f>(m, "vec3f")
    .def(py::init<float, float, float>(), py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0)
    .def_readwrite("x", &vec3f::x)
    .def_readwrite("y", &vec3f::y)
    .def_readwrite("z", &vec3f::z);
  // -----------------------------------------------------------------------------
  // VECTORS
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // INTEGER VECTORS
  // -----------------------------------------------------------------------------
  py::class_<vec2i>(m, "vec2i")
    .def(py::init<int, int>(), py::arg("x") = 0, py::arg("y") = 0)
    .def_readwrite("x", &vec2i::x)
    .def_readwrite("y", &vec2i::y);
  // -----------------------------------------------------------------------------
  // INTEGER VECTORS
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // RIGID BODY TRANSFORMS/FRAMES
  // -----------------------------------------------------------------------------
  py::class_<frame3f>(m, "frame3f")
    .def(py::init<vec3f, vec3f, vec3f, vec3f>(), 
        py::arg("x") = vec3f(1,0,0),
        py::arg("y") = vec3f(0,1,0),
        py::arg("z") = vec3f(0,0,1),
        py::arg("o") = vec3f(0,0,0))
    .def_readwrite("x", &frame3f::x)
    .def_readwrite("y", &frame3f::y)
    .def_readwrite("z", &frame3f::z)
    .def_readwrite("o", &frame3f::o);

  py::object py_identity3x4f = py::cast(identity3x4f);
  m.attr("identity3x4f")  = py_identity3x4f;
  // -----------------------------------------------------------------------------
  // RIGID BODY TRANSFORMS/FRAMES
  // -----------------------------------------------------------------------------

}


// -----------------------------------------------------------------------------
// YOCTO-IMAGE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_image, m) {

  // -----------------------------------------------------------------------------
  // IMAGE DATA AND UTILITIES
  // -----------------------------------------------------------------------------

  // py::class_<img::image>(m, "image")
  //   .def(py::init<int, img::shader_type, int, int, float, uint64_t, bool, int>(), 
  //       py::arg("resolution") = 720,
  //       py::arg("shader") = img::shader_type::path,
  //       py::arg("samples") = 512,
  //       py::arg("bounces") = 8,
  //       py::arg("clamp") = 100,
  //       py::arg("seed") = default_seed,
  //       py::arg("noparallel") = false,
  //       py::arg("pratio") = 8)
  //   .def_readwrite("resolution", &img::image::resolution)
  //   .def_readwrite("shader", &img::image::shader)
  //   .def_readwrite("samples", &img::image::samples)
  //   .def_readwrite("bounces", &img::image::bounces)
  //   .def_readwrite("clamp", &img::image::clamp)
  //   .def_readwrite("seed", &img::image::seed)
  //   .def_readwrite("noparallel", &img::image::noparallel)
  //   .def_readwrite("pratio", &img::image::pratio);

  // -----------------------------------------------------------------------------
  // IMAGE DATA AND UTILITIES
  // -----------------------------------------------------------------------------
}


// -----------------------------------------------------------------------------
// YOCTO-PATHTRACE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_pathtrace, m) {

  // -----------------------------------------------------------------------------
  // HIGH LEVEL API
  // -----------------------------------------------------------------------------
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
        py::arg("pratio") = 8)
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
  // -----------------------------------------------------------------------------
  // HIGH LEVEL API
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // SCENE AND RENDERING DATA
  // -----------------------------------------------------------------------------
  py::class_<ptr::camera> (m, "camera")
    .def(py::init<frame3f, float, vec2f, float, float>(),
        py::arg("frame") = identity3x4f,
        py::arg("lens") = 0.050,
        py::arg("film") = vec2f(0.036, 0.024),
        py::arg("focus") = 10000,
        py::arg("aperture") = 0)
    .def_readwrite("frame", &ptr::camera::frame)
    .def_readwrite("lens", &ptr::camera::lens)
    .def_readwrite("film", &ptr::camera::film)
    .def_readwrite("focus", &ptr::camera::focus)
    .def_readwrite("aperture", &ptr::camera::aperture)
    .def("nullptr", [](){
      return (ptr::camera*)nullptr;
    }, py::return_value_policy::reference);

  // py::class_<ptr::texture> (m, "texture")
  //   .def(py::init<img::image<vec3f>, img::image<vec3b>, img::image<float>, img::image<unsigned char>>(),
  //       py::arg("colorf") = img::image<vec3f>(),
  //       py::arg("colorb") = img::image<vec3b>(),
  //       py::arg("scalarf") = img::image<float>(),
  //       py::arg("scalarb") = img::image<unsigned char>())
  //   .def_readwrite("colorf", &ptr::texture::colorf)
  //   .def_readwrite("colorb", &ptr::texture::colorb)
  //   .def_readwrite("scalarf", &ptr::texture::scalarf)
  //   .def_readwrite("scalarb", &ptr::texture::scalarb)
  //   .def("nullptr", [](){
  //     return (ptr::texture*)nullptr;
  //   }, py::return_value_policy::reference);

  py::class_<ptr::scene>(m, "scene")
    .def(py::init<std::vector<ptr::camera*>,
                  std::vector<ptr::object*>,
                  std::vector<ptr::shape*>,
                  std::vector<ptr::material*>,
                  std::vector<ptr::texture*>,
                  std::vector<ptr::environment*>,
                  std::vector<ptr::light*>,
                  ptr::bvh_tree*>(), 
          py::arg("cameras") = std::vector<ptr::camera*>(),
          py::arg("objects") = std::vector<ptr::object*>(),
          py::arg("shapes") = std::vector<ptr::shape*>(),
          py::arg("materials") = std::vector<ptr::material*>(),
          py::arg("textures") = std::vector<ptr::texture*>(),
          py::arg("environments") = std::vector<ptr::environment*>(),
          py::arg("lights") = std::vector<ptr::light*>(),
          py::arg("bvh") = nullptr)
    .def_readwrite("cameras", &ptr::scene::cameras)
    .def_readwrite("objects", &ptr::scene::objects)
    .def_readwrite("shapes", &ptr::scene::shapes)
    .def_readwrite("materials", &ptr::scene::materials)
    .def_readwrite("textures", &ptr::scene::textures)
    .def_readwrite("environments", &ptr::scene::environments)
    .def_readwrite("lights", &ptr::scene::lights)
    .def_readwrite("bvh", &ptr::scene::bvh)
    .def("get", [](){
      return std::make_unique<ptr::scene>().get();
    }, py::return_value_policy::reference);
  // -----------------------------------------------------------------------------
  // SCENE AND RENDERING DATA
  // -----------------------------------------------------------------------------



  // -----------------------------------------------------------------------------
  // SCENE CREATION
  // -----------------------------------------------------------------------------
  // Add scene elements
  m.def("add_camera", &ptr::add_camera, py::arg("scene"), py::return_value_policy::reference);
  m.def("add_texture", &ptr::add_texture, py::arg("scene"), py::return_value_policy::reference);
  m.def("add_shape", &ptr::add_shape, py::arg("scene"), py::return_value_policy::reference);
  m.def("add_material", &ptr::add_material, py::arg("scene"), py::return_value_policy::reference);
  m.def("add_object", &ptr::add_object, py::arg("scene"), py::return_value_policy::reference);
  m.def("add_environment", &ptr::add_environment, py::arg("scene"), py::return_value_policy::reference);
  

  // camera properties
  m.def("set_frame", (void (*)(ptr::camera*, const frame3f&))&ptr::set_frame, py::arg("camera"), py::arg("frame"));
  m.def("set_lens", (void (*)(ptr::camera*, float, float, float))&ptr::set_lens, py::arg("camera"), py::arg("lens"), py::arg("aspect"), py::arg("film"));
  m.def("set_focus", (void (*)(ptr::camera*, float, float))&ptr::set_focus, py::arg("camera"), py::arg("aperture"), py::arg("focus"));

  // texture properties
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<vec3b>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<vec3f>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<byte>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<float>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  
  // shape properties
  m.def("set_points", &ptr::set_points, py::arg("shape"), py::arg("points"));
  m.def("set_lines", &ptr::set_lines, py::arg("shape"), py::arg("lines"));
  m.def("set_triangles", &ptr::set_triangles, py::arg("shape"), py::arg("triangles"));
  m.def("set_positions", &ptr::set_positions, py::arg("shape"), py::arg("positions"));
  m.def("set_normals", &ptr::set_normals, py::arg("shape"), py::arg("normals"));
  m.def("set_texcoords", &ptr::set_texcoords, py::arg("shape"), py::arg("texcoords"));
  m.def("set_radius", &ptr::set_radius, py::arg("shape"), py::arg("radius"));
  m.def("set_subdiv_quadspos", &ptr::set_subdiv_quadspos, py::arg("shape"), py::arg("quadspos"));
  m.def("set_subdiv_quadstexcoord", &ptr::set_subdiv_quadstexcoord, py::arg("shape"), py::arg("quadstexcoords"));
  m.def("set_subdiv_positions", &ptr::set_subdiv_positions, py::arg("shape"), py::arg("positions"));
  m.def("set_subdiv_texcoords", &ptr::set_subdiv_texcoords, py::arg("shape"), py::arg("texcoords"));
  m.def("set_subdiv_subdivision", &ptr::set_subdiv_subdivision, py::arg("shape"), py::arg("level"), py::arg("smooth"));
  m.def("set_subdiv_displacement", &ptr::set_subdiv_displacement, py::arg("shape"), py::arg("displacement"), py::arg("displacement_tex"));

  // material properties
  m.def("set_emission", (void (*)(ptr::material*, const vec3f&, ptr::texture*))&ptr::set_emission, py::arg("material"), py::arg("emission"), py::arg("emission_tex"));
  m.def("set_color", &ptr::set_color, py::arg("material"), py::arg("color"), py::arg("color_tex"));
  m.def("set_specular", &ptr::set_specular, py::arg("material"), py::arg("specular"), py::arg("specular_tex"));
  m.def("set_metallic", &ptr::set_metallic, py::arg("material"), py::arg("metallic"), py::arg("metallic_tex"));
  m.def("set_ior", &ptr::set_ior, py::arg("material"), py::arg("ior"));
  m.def("set_transmission", &ptr::set_transmission, py::arg("material"), py::arg("transmission"), py::arg("thin"), py::arg("trdepth"), py::arg("transmission_tex"));
  m.def("set_thin", &ptr::set_thin, py::arg("material"), py::arg("thin"));
  m.def("set_roughness", &ptr::set_roughness, py::arg("material"), py::arg("roughness"), py::arg("roughness_tex"));
  m.def("set_opacity", &ptr::set_opacity, py::arg("material"), py::arg("opacity"), py::arg("opacity_tex"));
  m.def("set_scattering", &ptr::set_scattering, py::arg("material"), py::arg("scattering"), py::arg("scanisotropy"), py::arg("scattering_tex"));
  m.def("set_normalmap", &ptr::set_normalmap, py::arg("material"), py::arg("normal_tex"));
  

  // add environment
  m.def("set_emission", (void (*)(ptr::environment*, const vec3f&, ptr::texture*))&ptr::set_emission, py::arg("environment"), py::arg("emission"), py::arg("emission_tex"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<vec3b>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<vec3f>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<unsigned char>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  m.def("set_texture", (void (*)(ptr::texture*, const img::image<float>&))&ptr::set_texture, py::arg("texture"), py::arg("img"));
  // -----------------------------------------------------------------------------
  // SCENE CREATION
  // -----------------------------------------------------------------------------
}


// -----------------------------------------------------------------------------
// YOCTO COMMONIO
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_commonio, m) {

  // -----------------------------------------------------------------------------
  // IMPLEMENTATION OF COMMAND-LINE PARSING
  // -----------------------------------------------------------------------------
  py::enum_<cli::cli_type>(m, "cli_type")
    .value("string_", cli::cli_type::string_)
    .value("int_", cli::cli_type::int_)
    .value("float_", cli::cli_type::float_)
    .value("bool_", cli::cli_type::bool_)
    .value("flag_", cli::cli_type::flag_)
    .value("string_vector_", cli::cli_type::string_vector_)
    .value("enum_", cli::cli_type::enum_)
    .export_values(); 

  py::class_<cli::cmdline_option>(m, "cmdline_option")
    .def(py::init<std::string, std::string, cli::cli_type, void*, bool, bool, std::vector<std::string>>(), 
        py::arg("name") = "",
        py::arg("usage") = "",
        py::arg("type") = cli::cli_type::string_,
        py::arg("value") = py::cast<void *>(nullptr), // py::cast<void *>(nullptr),
        py::arg("req") = false,
        py::arg("set") = false,
        py::arg("choices") = std::vector<std::string>())
    .def_readwrite("name", &cli::cmdline_option::name)
    .def_readwrite("usage", &cli::cmdline_option::usage)
    .def_readwrite("type", &cli::cmdline_option::type)
    .def_readwrite("value", &cli::cmdline_option::value)
    .def_readwrite("req", &cli::cmdline_option::req)
    .def_readwrite("set", &cli::cmdline_option::set)
    .def_readwrite("choices", &cli::cmdline_option::choices);

  py::class_<cli::cli_state>(m, "cli_state")
    .def(py::init<std::string, std::string, std::vector<cli::cmdline_option>, std::string, std::string, bool>(), 
        py::arg("name") = "",
        py::arg("usage") = "",
        py::arg("options") = std::vector<cli::cmdline_option>(),
        py::arg("usage_options") = "",
        py::arg("usage_arguments") = "",
        py::arg("help") = false)
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
    std::vector<const char *> cstrs; //(argv.size() + 1);

    // make the pointers point to the C strings in the std::strings in the
    // std::vector
    for (auto &s : argv) cstrs.push_back((char *)(s.c_str()));
    // for(size_t i = 0; i < argv.size(); ++i) {
    //     cstrs[i] = argv[i].data();
    // }
    
    // add a terminating nullptr (main wants that, so perhaps the closed source
    // function wants it too)
    // cstrs[argv.size()] = nullptr;

    // call the closed source function
    return cli::parse_cli(cli, static_cast<int>(cstrs.size()), cstrs.data());
  });

  m.def("print_progress", &cli::print_progress, py::arg("message"), py::arg("current"), py::arg("total"));
  m.def("print_fatal", &cli::print_fatal, py::arg("msg"));


}


// -----------------------------------------------------------------------------
// YOCTO SCENEIO
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_sceneio, m) {

  // -----------------------------------------------------------------------------
  // SCENE DATA
  // -----------------------------------------------------------------------------
  py::class_<sio::camera> (m, "camera")
    .def(py::init<std::string, frame3f, bool, float, float, float, float, float>(),
        py::arg("name") = "",
        py::arg("frame") = identity3x4f,
        py::arg("orthographic") = false,
        py::arg("lens") = 0.050,
        py::arg("film") = 0.036, 
        py::arg("aspect") = 1.500,
        py::arg("focus") = 10000,
        py::arg("aperture") = 0)
    .def_readwrite("name", &sio::camera::name)
    .def_readwrite("frame", &sio::camera::frame)
    .def_readwrite("orthographic", &sio::camera::orthographic)
    .def_readwrite("lens", &sio::camera::lens)
    .def_readwrite("film", &sio::camera::film)
    .def_readwrite("aspect", &sio::camera::aspect)
    .def_readwrite("focus", &sio::camera::focus)
    .def_readwrite("aperture", &sio::camera::aperture)
    .def("nullptr", [](){
      return (sio::camera*)nullptr;
    }, py::return_value_policy::reference);

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
          py::arg("cameras") = std::vector<sio::camera*>(),
          py::arg("objects") = std::vector<sio::object*>(),
          py::arg("environments") = std::vector<sio::environment*>(),
          py::arg("shapes") = std::vector<sio::shape*>(),
          py::arg("subdivs") = std::vector<sio::subdiv*>(),
          py::arg("textures") = std::vector<sio::texture*>(),
          py::arg("materials") = std::vector<sio::material*>(),
          py::arg("instances") = std::vector<sio::instance*>(),
          py::arg("name") = "",
          py::arg("copyright") = "")
    .def_readwrite("cameras", &sio::model::cameras)
    .def_readwrite("objects", &sio::model::objects)
    .def_readwrite("environments", &sio::model::environments)
    .def_readwrite("shapes", &sio::model::shapes)
    .def_readwrite("subdivs", &sio::model::subdivs)
    .def_readwrite("textures", &sio::model::textures)
    .def_readwrite("materials", &sio::model::materials)
    .def_readwrite("instances", &sio::model::instances)
    .def_readwrite("name", &sio::model::name)
    .def_readwrite("copyright", &sio::model::copyright)
    .def("get", [](){
      auto ioscene_guard =  std::make_unique<sio::model>();
      return ioscene_guard.get();
    }, py::return_value_policy::reference);
  // -----------------------------------------------------------------------------
  // SCENE DATA
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // SCENE IO FUNCTIONS
  // -----------------------------------------------------------------------------

  // const py::object progress_callback = py::cast(sio::progress_callback);
  // m.attr("progress_callback") = progress_callback;

  m.def("get_camera", &sio::get_camera, py::arg("scene"), py::arg("name") = "", py::return_value_policy::reference);

  m.def("load_scene", &sio::load_scene, py::arg("filename"), py::arg("scene"), py::arg("error"),
      py::arg("progress_cb") = std::function<void(const std::string&, int, int)>(), py::arg("noparallel") = false);
  // -----------------------------------------------------------------------------
  // SCENE IO FUNCTIONS
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // EXAMPLE SCENES
  // -----------------------------------------------------------------------------
  m.def("make_cornellbox", &sio::make_cornellbox);
  // -----------------------------------------------------------------------------
  // EXAMPLE SCENES
  // -----------------------------------------------------------------------------

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