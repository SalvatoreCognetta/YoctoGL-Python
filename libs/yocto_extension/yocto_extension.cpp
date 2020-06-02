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
  // MATH CONSTANTS AND FUNCTIONS
  // -----------------------------------------------------------------------------
  m.attr("pif")  = pif;
  // -----------------------------------------------------------------------------
  // MATH CONSTANTS AND FUNCTIONS
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // VECTORS
  // -----------------------------------------------------------------------------
  py::class_<vec2f>(m, "vec2f")
    .def(py::init<float, float>(), 
        py::arg("x") = 0, py::arg("y") = 0)
    .def_readwrite("x", &vec2f::x)
    .def_readwrite("y", &vec2f::y);

  py::class_<vec3f>(m, "vec3f")
    .def(py::init<float, float, float>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0)
    .def_readwrite("x", &vec3f::x)
    .def_readwrite("y", &vec3f::y)
    .def_readwrite("z", &vec3f::z);

  py::class_<vec4f>(m, "vec4f")
    .def(py::init<float, float, float, float>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0, py::arg("w") = 0)
    .def_readwrite("x", &vec4f::x)
    .def_readwrite("y", &vec4f::y)
    .def_readwrite("z", &vec4f::z)
    .def_readwrite("w", &vec4f::w);

  py::object py_zero2f = py::cast(zero2f);
  m.attr("zero2f")  = py_zero2f;
  py::object py_zero3f = py::cast(zero3f);
  m.attr("zero3f")  = py_zero3f;
  py::object py_zero4f = py::cast(zero4f);
  m.attr("zero4f")  = py_zero4f;
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

  py::class_<vec3i>(m, "vec3i")
    .def(py::init<int, int, int>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0)
    .def_readwrite("x", &vec3i::x)
    .def_readwrite("y", &vec3i::y)
    .def_readwrite("z", &vec3i::z);

  py::class_<vec4i>(m, "vec4i")
    .def(py::init<int, int, int, int>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0, py::arg("w") = 0)
    .def_readwrite("x", &vec4i::x)
    .def_readwrite("y", &vec4i::y)
    .def_readwrite("z", &vec4i::z)
    .def_readwrite("w", &vec4i::w);

  py::class_<vec3b>(m, "vec3b")
    .def(py::init<unsigned char, unsigned char, unsigned char>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0)
    .def_readwrite("x", &vec3b::x)
    .def_readwrite("y", &vec3b::y)
    .def_readwrite("z", &vec3b::z);

  py::class_<vec4b>(m, "vec4b")
    .def(py::init<unsigned char, unsigned char, unsigned char, unsigned char>(), 
        py::arg("x") = 0, py::arg("y") = 0, py::arg("z") = 0, py::arg("w") = 0)
    .def_readwrite("x", &vec4b::x)
    .def_readwrite("y", &vec4b::y)
    .def_readwrite("z", &vec4b::z)
    .def_readwrite("w", &vec4b::w);

  py::object py_zero2i = py::cast(zero2i);
    m.attr("zero2i")  = py_zero2i;
  py::object py_zero3i = py::cast(zero3i);
    m.attr("zero3i")  = py_zero3i;
  py::object py_zero4i = py::cast(zero4i);
    m.attr("zero4i")  = py_zero4i;
  py::object py_zero3b = py::cast(math::zero3b);
    m.attr("zero3b")  = py_zero3b;
  py::object py_zero4b = py::cast(math::zero4b);
    m.attr("zero4b")  = py_zero4b;
  // -----------------------------------------------------------------------------
  // INTEGER VECTORS
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // RIGID BODY TRANSFORMS/FRAMES
  // -----------------------------------------------------------------------------
  // py::class_<frame2f>(m, "frame2f")
  //   .def(py::init<vec2f, vec2f, vec2f>(), 
  //       py::arg("x") = vec2f(1,0),
  //       py::arg("y") = vec2f(0,1),
  //       py::arg("o") = vec2f(0,0))
  //   .def_readwrite("x", &frame3f::x)
  //   .def_readwrite("y", &frame3f::y)
  //   .def_readwrite("o", &frame3f::o);

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
  
  // py::object py_identity2x3f = py::cast(identity2x3f);
  // m.attr("identity3x4f")  = py_identity2x3f;

  py::object py_identity3x4f = py::cast(identity3x4f);
  m.attr("identity3x4f")  = py_identity3x4f;
  // -----------------------------------------------------------------------------
  // RIGID BODY TRANSFORMS/FRAMES
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // RANDOM NUMBER GENERATION
  // -----------------------------------------------------------------------------
  py::class_<rng_state>(m, "rng_state")
    .def(py::init<uint64_t, uint64_t>(), 
        py::arg("state") = 0x853c49e6748fea9bULL,
        py::arg("inc") = 0xda3e39cb94b95bdbULL)
    .def_readwrite("state", &rng_state::state)
    .def_readwrite("inc", &rng_state::inc);
  // -----------------------------------------------------------------------------
  // RANDOM NUMBER GENERATION
  // -----------------------------------------------------------------------------

}


// -----------------------------------------------------------------------------
// YOCTO-SHAPE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_shape, m) {

  // -----------------------------------------------------------------------------
  // SHAPE ELEMENT CONVERSION AND GROUPING
  // -----------------------------------------------------------------------------
  m.def("quads_to_triangles", &shp::quads_to_triangles, py::return_value_policy::reference);
  m.def("triangles_to_quads", &shp::triangles_to_quads, py::return_value_policy::reference);
  // m.def("bezier_to_lines", &shp::bezier_to_lines, py::return_value_policy::reference);
  // -----------------------------------------------------------------------------
  // SHAPE ELEMENT CONVERSION AND GROUPING
  // -----------------------------------------------------------------------------

}


// -----------------------------------------------------------------------------
// YOCTO-IMAGE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_image, m) {

  // -----------------------------------------------------------------------------
  // IMAGE DATA AND UTILITIES
  // -----------------------------------------------------------------------------
  py::class_<img::image<vec2f>>(m, "image_vec2f")
    .def(py::init<>())
    .def("size", [](img::image<vec2f> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<vec3f>>(m, "image_vec3f")
    .def(py::init<>())
    .def("size", [](img::image<vec3f> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<vec4f>>(m, "image_vec4f")
    .def(py::init<>())
    .def("size", [](img::image<vec4f> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<vec3b>>(m, "image_vec3b")
    .def(py::init<>())
    .def("size", [](img::image<vec3b> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<vec4b>>(m, "image_vec4b")
    .def(py::init<>())
    .def("size", [](img::image<vec4b> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<float>>(m, "image_float")
    .def(py::init<>())
    .def("size", [](img::image<float> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<unsigned char>>(m, "image_byte")
    .def(py::init<>())
    .def("size", [](img::image<unsigned char> image) -> vec2i {
      return image.size();
    });
  py::class_<img::image<ptr::pixel>>(m, "image_pixel")
    .def(py::init<>())
    .def("size", [](img::image<ptr::pixel> image) -> vec2i {
      return image.size();
    });
  // -----------------------------------------------------------------------------
  // IMAGE DATA AND UTILITIES
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // IMAGE UTILITIES
  // -----------------------------------------------------------------------------
  // Conversion between linear and gamma-encoded images.
  m.def("srgb_to_rgb", (img::image<vec4f> (*)(const img::image<vec4f>&))&img::srgb_to_rgb, 
    py::arg("srgb"));
  m.def("rgb_to_srgb", (img::image<vec4f> (*)(const img::image<vec4f>&))&img::rgb_to_srgb, 
    py::arg("rgb"));
  m.def("srgb_to_rgb", (img::image<vec4f> (*)(const img::image<vec4b>&))&img::srgb_to_rgb, 
    py::arg("srgb"));
  m.def("rgb_to_srgbb", (img::image<vec4b> (*)(const img::image<vec4f>&))&img::rgb_to_srgbb, 
    py::arg("rgb"));
  m.def("srgb_to_rgb", (img::image<vec3f> (*)(const img::image<vec3f>&))&img::srgb_to_rgb, 
    py::arg("srgb"));
  m.def("rgb_to_srgb", (img::image<vec3f> (*)(const img::image<vec3f>&))&img::rgb_to_srgb, 
    py::arg("rgb"));
  // -----------------------------------------------------------------------------
  // IMAGE UTILITIES
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // IMAGE IO
  // -----------------------------------------------------------------------------
  m.def("is_hdr_filename", &img::is_hdr_filename, py::arg("filename"));

  m.def("load_image", (bool (*)(const std::string&, img::image<vec4f>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<vec4f>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("load_image", (bool (*)(const std::string&, img::image<vec4b>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<vec4b>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));

  m.def("load_image", (bool (*)(const std::string&, img::image<vec3f>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<vec3f>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("load_image", (bool (*)(const std::string&, img::image<vec3b>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<vec3b>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));

  m.def("load_image", (bool (*)(const std::string&, img::image<float>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<float>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("load_image", (bool (*)(const std::string&, img::image<unsigned char>&, std::string&))&img::load_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));
  m.def("save_image", (bool (*)(const std::string&, const img::image<unsigned char>&, std::string&))&img::save_image,
    py::arg("filename"), py::arg("img"), py::arg("error"));

  // m.def("save_image_vec4f", [](const std::string& filename, const img::image<vec4f>& img, std::string& error) -> bool {
  //   return img::save_image(filename, img, error);
  // });
  // m.def("save_image_vec3f", [](const std::string& filename, const img::image<vec3f>& img, std::string& error) -> bool {
  //   return img::save_image(filename, img, error);
  // });
  // m.def("save_image_float", [](const std::string& filename, const img::image<float>& img, std::string& error) -> bool {
  //   return img::save_image(filename, img, error);
  // });  
  // -----------------------------------------------------------------------------
  // IMAGE IO
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // EXAMPLE IMAGES
  // -----------------------------------------------------------------------------
  m.def("make_grid", &img::make_grid, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0.2, 0.2, 0.2, 1), py::arg("color1") = vec4f(0.5, 0.5, 0.5, 1));
  m.def("make_checker", &img::make_checker, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0.2, 0.2, 0.2, 1), py::arg("color1") = vec4f(0.5, 0.5, 0.5, 1));
  m.def("make_bumps", &img::make_bumps, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0, 0, 0, 1), py::arg("color1") = vec4f(1, 1, 1, 1));
  m.def("make_ramp", &img::make_ramp, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0, 0, 0, 1), py::arg("color1") = vec4f(1, 1, 1, 1));
  m.def("make_gammaramp", &img::make_gammaramp, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0, 0, 0, 1), py::arg("color1") = vec4f(1, 1, 1, 1));
  m.def("make_uvramp", &img::make_uvramp, py::arg("img"), py::arg("size"), py::arg("scale") = 1);
  m.def("make_uvgrid", &img::make_uvgrid, py::arg("img"), py::arg("size"), py::arg("scale") = 1,
    py::arg("colored") = true);
  m.def("make_blackbodyramp", &img::make_blackbodyramp, py::arg("img"), py::arg("size"), py::arg("scale") = 1,
    py::arg("from") = 1000, py::arg("from") = 12000);
  m.def("make_noisemap", &img::make_noisemap, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("color0") = vec4f(0, 0, 0, 1), py::arg("color1") = vec4f(0, 0, 0, 1));
  m.def("make_fbmmap", &img::make_fbmmap, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("noise") = vec4f(2, 0.5, 8, 1), py::arg("color0") = vec4f(0, 0, 0, 1),
    py::arg("color1") = vec4f(0, 0, 0, 1));
  m.def("make_turbulencemap", &img::make_turbulencemap, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("noise") = vec4f(2, 0.5, 8, 1), py::arg("color0") = vec4f(0, 0, 0, 1),
    py::arg("color1") = vec4f(0, 0, 0, 1));
  m.def("make_ridgemap", &img::make_ridgemap, py::arg("img"), py::arg("size"), py::arg("scale") = 1, 
    py::arg("noise") = vec4f(2, 0.5, 8, 1), py::arg("color0") = vec4f(0, 0, 0, 1),
    py::arg("color1") = vec4f(0, 0, 0, 1));

  m.def("make_sunsky", &img::make_sunsky, py::arg("img"), py::arg("size"), py::arg("sun_angle"),
    py::arg("turbidity") = 3, py::arg("has_sun") = false, py::arg("sun_intensity") = 1,
    py::arg("sun_radius") = 1, py::arg("ground_albedo") = vec3f(0.2, 0.2, 0.2));
  m.def("make_lights", &img::make_lights, py::arg("img"), py::arg("size"),
    py::arg("le") = vec3f(1, 1, 1), py::arg("nlights") = 4, py::arg("langle") = pif / 4,
    py::arg("lwidth") = pif / 16, py::arg("lheight") = pif / 16);

  m.def("bump_to_normal", (img::image<vec4f> (*)(const img::image<vec4f>&, float))&img::bump_to_normal, 
    py::arg("img"), py::arg("scale") = 1);
  // -----------------------------------------------------------------------------
  // EXAMPLE IMAGES
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

  m.def("init_bvh", (void (*)(ptr::scene*, const ptr::trace_params&, std::function<void(const std::string&, int, int)>))&ptr::init_bvh,
      py::arg("scene"), py::arg("params"), py::arg("progress_cb") = std::function<void(const std::string&, int, int)>());
  m.def("init_state", &ptr::init_state, py::arg("state"), py::arg("scene"), py::arg("camera"), py::arg("params"));
  m.def("init_lights", &ptr::init_lights, py::arg("scene"), py::arg("params"), py::arg("progress_cb"));
  m.def("init_subdivs", &ptr::init_subdivs, py::arg("scene"), py::arg("params"), py::arg("progress_cb"));
  m.def("trace_samples", (void (*)(ptr::state*, const ptr::scene*, const ptr::camera*, const ptr::trace_params&))&ptr::trace_samples,
      py::arg("state"), py::arg("scene"), py::arg("camera"), py::arg("params"));
  m.def("trace_samples", (void (*)(ptr::state*, const ptr::scene*, const ptr::camera*, const ptr::trace_params&, std::atomic<bool>*))&ptr::trace_samples,
      py::arg("state"), py::arg("scene"), py::arg("camera"), py::arg("params"), py::arg("stop"));
  // -----------------------------------------------------------------------------
  // HIGH LEVEL API
  // -----------------------------------------------------------------------------


  // -----------------------------------------------------------------------------
  // SCENE AND RENDERING DATA
  // -----------------------------------------------------------------------------
  py::class_<ptr::bvh_node>(m, "bvh_node")
    .def_readwrite("bbox", &ptr::bvh_node::bbox)
    .def_readwrite("start", &ptr::bvh_node::start)
    .def_readwrite("num", &ptr::bvh_node::num)
    .def_readwrite("internal", &ptr::bvh_node::internal)
    .def_readwrite("axis", &ptr::bvh_node::axis);

  py::class_<ptr::bvh_tree>(m, "bvh_tree")
    .def(py::init<std::vector<ptr::bvh_node>, std::vector<int>>(),
        py::arg("nodes") = std::vector<ptr::bvh_node>(),
        py::arg("primitives") = std::vector<int>())
    .def_readwrite("nodes", &ptr::bvh_tree::nodes)
    .def_readwrite("primitives", &ptr::bvh_tree::primitives);

  py::class_<ptr::camera>(m, "camera")
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

  py::class_<ptr::texture>(m, "texture")
    .def(py::init<img::image<vec3f>, img::image<vec3b>, img::image<float>, img::image<unsigned char>>(),
        py::arg("colorf") = img::image<vec3f>(),
        py::arg("colorb") = img::image<vec3b>(),
        py::arg("scalarf") = img::image<float>(),
        py::arg("scalarb") = img::image<unsigned char>())
    .def_readwrite("colorf", &ptr::texture::colorf)
    .def_readwrite("colorb", &ptr::texture::colorb)
    .def_readwrite("scalarf", &ptr::texture::scalarf)
    .def_readwrite("scalarb", &ptr::texture::scalarb)
    .def("nullptr", [](){
      return (ptr::texture*)nullptr;
    }, py::return_value_policy::reference);

  py::class_<ptr::scene>(m, "scene")
    .def(py::init<std::vector<ptr::camera*>, std::vector<ptr::object*>,
                  std::vector<ptr::shape*>, std::vector<ptr::material*>,
                  std::vector<ptr::texture*>, std::vector<ptr::environment*>,
                  std::vector<ptr::light*>, ptr::bvh_tree*>(), 
          py::arg("cameras") = std::vector<ptr::camera*>(),
          py::arg("objects") = std::vector<ptr::object*>(),
          py::arg("shapes") = std::vector<ptr::shape*>(),
          py::arg("materials") = std::vector<ptr::material*>(),
          py::arg("textures") = std::vector<ptr::texture*>(),
          py::arg("environments") = std::vector<ptr::environment*>(),
          py::arg("lights") = std::vector<ptr::light*>(),
          py::arg("bvh") = py::cast<ptr::bvh_tree *>(nullptr))
    .def_readwrite("cameras", &ptr::scene::cameras)
    .def_readwrite("objects", &ptr::scene::objects)
    .def_readwrite("shapes", &ptr::scene::shapes)
    .def_readwrite("materials", &ptr::scene::materials)
    .def_readwrite("textures", &ptr::scene::textures)
    .def_readwrite("environments", &ptr::scene::environments)
    .def_readwrite("lights", &ptr::scene::lights)
    .def_readwrite("bvh", &ptr::scene::bvh)
    .def("get", []() -> ptr::scene* {
      auto scene_guard =  std::unique_ptr<ptr::scene>(new ptr::scene());
      // auto scene_guard = std::make_unique<ptr::scene>().get()
      return scene_guard.get();
    }, py::return_value_policy::reference);

  py::class_<ptr::pixel>(m, "pixel")
    .def(py::init<vec4f, int, math::rng_state>(),
        py::arg("accumulated") = vec4f(0,0,0,0),
        py::arg("samples") = 0,
        py::arg("rng") = math::rng_state())
    .def_readwrite("accumulated", &ptr::pixel::accumulated)
    .def_readwrite("samples", &ptr::pixel::samples)
    .def_readwrite("rng", &ptr::pixel::rng);

  py::class_<ptr::state>(m, "state")
    .def(py::init<img::image<vec4f>, img::image<ptr::pixel>>(),
        py::arg("render") = img::image<vec4f>(),
        py::arg("pixels") = img::image<ptr::pixel>())
    .def_readwrite("render", &ptr::state::render)
    .def_readwrite("pixels", &ptr::state::pixels);
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
  
  // object properties
  m.def("set_frame", (void (*)(ptr::object*, const frame3f&))&ptr::set_frame, py::arg("object"), py::arg("frame"));
  m.def("set_shape", &ptr::set_shape, py::arg("object"), py::arg("shape"));
  m.def("set_material", &ptr::set_material, py::arg("object"), py::arg("material"));

  // shape properties
  m.def("set_points", &ptr::set_points, py::arg("shape"), py::arg("points"));
  m.def("set_lines", &ptr::set_lines, py::arg("shape"), py::arg("lines"));
  m.def("set_triangles", &ptr::set_triangles, py::arg("shape"), py::arg("triangles"));
  m.def("set_positions", &ptr::set_positions, py::arg("shape"), py::arg("positions"));
  m.def("set_normals", &ptr::set_normals, py::arg("shape"), py::arg("normals"));
  m.def("set_texcoords", &ptr::set_texcoords, py::arg("shape"), py::arg("texcoords"));
  m.def("set_radius", &ptr::set_radius, py::arg("shape"), py::arg("radius"));

  // subdiv properties
  m.def("set_subdiv_quadspos", &ptr::set_subdiv_quadspos, py::arg("shape"), py::arg("quadspos"));
  m.def("set_subdiv_quadstexcoord", &ptr::set_subdiv_quadstexcoord, py::arg("shape"), py::arg("quadstexcoord"));
  m.def("set_subdiv_positions", &ptr::set_subdiv_positions, py::arg("shape"), py::arg("positions"));
  m.def("set_subdiv_texcoords", &ptr::set_subdiv_texcoords, py::arg("shape"), py::arg("texcoords"));
  m.def("set_subdiv_subdivision", &ptr::set_subdiv_subdivision, py::arg("shape"), py::arg("level"), py::arg("smooth"));
  m.def("set_subdiv_displacement", &ptr::set_subdiv_displacement, py::arg("shape"), py::arg("displacement"), py::arg("displacement_tex"));

  // material properties
  m.def("set_emission", (void (*)(ptr::material*, const vec3f&, ptr::texture*))&ptr::set_emission, py::arg("material"), py::arg("emission"), py::arg("emission_tex") = nullptr);
  m.def("set_color", &ptr::set_color, py::arg("material"), py::arg("color"), py::arg("color_tex") = nullptr);
  m.def("set_specular", &ptr::set_specular, py::arg("material"), py::arg("specular") = 1, py::arg("specular_tex") = nullptr);
  m.def("set_metallic", &ptr::set_metallic, py::arg("material"), py::arg("metallic"), py::arg("metallic_tex") = nullptr);
  m.def("set_ior", &ptr::set_ior, py::arg("material"), py::arg("ior"));
  m.def("set_transmission", &ptr::set_transmission, py::arg("material"), py::arg("transmission"), py::arg("thin"), py::arg("trdepth"), py::arg("transmission_tex") = nullptr);
  m.def("set_roughness", &ptr::set_roughness, py::arg("material"), py::arg("roughness"), py::arg("roughness_tex") = nullptr);
  m.def("set_opacity", &ptr::set_opacity, py::arg("material"), py::arg("opacity"), py::arg("opacity_tex") = nullptr);
  m.def("set_thin", &ptr::set_thin, py::arg("material"), py::arg("thin"));
  m.def("set_scattering", &ptr::set_scattering, py::arg("material"), py::arg("scattering"), py::arg("scanisotropy"), py::arg("scattering_tex") = nullptr);
  m.def("set_normalmap", &ptr::set_normalmap, py::arg("material"), py::arg("normal_tex"));

  // environment properties
  m.def("set_frame", (void (*)(ptr::environment*, const frame3f&))&ptr::set_frame, py::arg("environment"), py::arg("frame"));

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
        py::arg("value") = py::cast<void *>(nullptr), // py::arg("value").none(false) = py::cast<void *>(nullptr),
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
  m.def("print_info", &cli::print_info, py::arg("msg"));
  m.def("print_fatal", &cli::print_fatal, py::arg("msg"));


}


// -----------------------------------------------------------------------------
// YOCTO SCENEIO
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_sceneio, m) {

  // -----------------------------------------------------------------------------
  // SCENE DATA
  // -----------------------------------------------------------------------------
  py::class_<sio::camera>(m, "camera")
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

  py::class_<sio::texture>(m, "texture")
    // .def(py::init<std::string, img::image<vec3f>, img::image<vec3b>, img::image<float>, img::image<unsigned char>>(),
    //     py::arg("name") = "",
    //     py::arg("colorf") = img::image<vec3f>(),
    //     py::arg("colorb") = img::image<vec3b>(),
    //     py::arg("scalarf") = img::image<float>(),
    //     py::arg("scalarb") = img::image<unsigned char>())
    .def_readwrite("name", &sio::texture::name)
    .def_readwrite("colorf", &sio::texture::colorf)
    .def_readwrite("colorb", &sio::texture::colorb)
    .def_readwrite("scalarf", &sio::texture::scalarf)
    .def_readwrite("scalarb", &sio::texture::scalarb);

  m.def("texture_empty", [](sio::texture* iotexture, std::string param) {
    if (param.compare("colorf"))
      return iotexture->colorf.empty();
    else if (param.compare("colorb"))
      return iotexture->colorb.empty();
    else if (param.compare("scalarf"))
      return iotexture->scalarf.empty();
    else if (param.compare("scalarb"))
      return iotexture->scalarb.empty();
    return true;    
  });

  py::class_<sio::material>(m, "material")
    .def(py::init<std::string, vec3f, vec3f, float, float, float, float, vec3f, 
                  float, float, float, vec3f, float, float, float, float, bool,
                  sio::texture*, sio::texture*, sio::texture*, sio::texture*, 
                  sio::texture*, sio::texture*, sio::texture*, sio::texture*, 
                  sio::texture*, sio::texture*, sio::texture*, sio::texture*, 
                  sio::texture*, int, bool>(),
        // material data
        py::arg("name") = "",
        // material
        py::arg("emission") = vec3f(0,0,0),
        py::arg("color") = vec3f(0,0,0),
        py::arg("specular") = 0,
        py::arg("roughness") = 0, 
        py::arg("metallic") = 0, 
        py::arg("ior") = 1.5,
        py::arg("spectint") = vec3f(1,1,1),
        py::arg("coat") = 0,
        py::arg("transmission") = 0,
        py::arg("translucency") = 0,
        py::arg("scattering") = vec3f(0,0,0),
        py::arg("scanisotropy") = 0,
        py::arg("trdepth") = 0.01,
        py::arg("opacity") = 1,
        py::arg("displacement") = 0,
        py::arg("thin") = true,
        // textures
        py::arg("emission_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("color_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("specular_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("metallic_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("roughness_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("transmission_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("translucency_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("spectint_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("scattering_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("coat_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("opacity_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("normal_tex") = py::cast<sio::texture*>(nullptr),
        py::arg("displacement_tex") = py::cast<sio::texture*>(nullptr),
        // [experimental] properties to drive subdiv and displacement
        py::arg("subdivisions") = 2,
        py::arg("smooth") = true)
    .def_readwrite("name", &sio::material::name)
    .def_readwrite("emission", &sio::material::emission)
    .def_readwrite("color", &sio::material::color)
    .def_readwrite("specular", &sio::material::specular)
    .def_readwrite("roughness", &sio::material::roughness)
    .def_readwrite("metallic", &sio::material::metallic)
    .def_readwrite("ior", &sio::material::ior)
    .def_readwrite("spectint", &sio::material::spectint)
    .def_readwrite("coat", &sio::material::coat)
    .def_readwrite("transmission", &sio::material::transmission)
    .def_readwrite("translucency", &sio::material::translucency)
    .def_readwrite("scattering", &sio::material::scattering)
    .def_readwrite("scanisotropy", &sio::material::scanisotropy)
    .def_readwrite("trdepth", &sio::material::trdepth)
    .def_readwrite("opacity", &sio::material::opacity)
    .def_readwrite("displacement", &sio::material::displacement)
    .def_readwrite("thin", &sio::material::thin)
    .def_readwrite("emission_tex", &sio::material::emission_tex)
    .def_readwrite("color_tex", &sio::material::color_tex)
    .def_readwrite("specular_tex", &sio::material::specular_tex)
    .def_readwrite("metallic_tex", &sio::material::metallic_tex)
    .def_readwrite("roughness_tex", &sio::material::roughness_tex)
    .def_readwrite("transmission_tex", &sio::material::transmission_tex)
    .def_readwrite("translucency_tex", &sio::material::translucency_tex)
    .def_readwrite("spectint_tex", &sio::material::spectint_tex)
    .def_readwrite("scattering_tex", &sio::material::scattering_tex)
    .def_readwrite("coat_tex", &sio::material::coat_tex)
    .def_readwrite("opacity_tex", &sio::material::opacity_tex)
    .def_readwrite("normal_tex", &sio::material::normal_tex)
    .def_readwrite("displacement_tex", &sio::material::displacement_tex)
    .def_readwrite("subdivisions", &sio::material::subdivisions)
    .def_readwrite("smooth", &sio::material::smooth);
  
  py::class_<sio::shape>(m, "shape")
    .def(py::init<std::string, std::vector<int>, std::vector<vec2i>,
                  std::vector<vec3i>, std::vector<vec4i>, std::vector<vec3f>,
                  std::vector<vec3f>, std::vector<vec2f>, std::vector<vec3f>,
                  std::vector<float>, std::vector<vec4f>>(),
        // shape data
        py::arg("name") = "",
        // primitives
        py::arg("points") = std::vector<int>(),
        py::arg("lines") = std::vector<vec2i>(),
        py::arg("triangles") = std::vector<vec3i>(),
        py::arg("quads") = std::vector<vec4i>(),
        // vertex data
        py::arg("positions") = std::vector<vec3f>(),
        py::arg("normals") = std::vector<vec3f>(),
        py::arg("texcoords") = std::vector<vec2f>(),
        py::arg("colors") = std::vector<vec3f>(),
        py::arg("radius") = std::vector<float>(),
        py::arg("tangents") = std::vector<vec4f>())
    .def_readwrite("name", &sio::shape::name)
    .def_readwrite("points", &sio::shape::points)
    .def_readwrite("lines", &sio::shape::lines)
    .def_readwrite("triangles", &sio::shape::triangles)
    .def_readwrite("quads", &sio::shape::quads)
    .def_readwrite("positions", &sio::shape::positions)
    .def_readwrite("normals", &sio::shape::normals)
    .def_readwrite("texcoords", &sio::shape::texcoords)
    .def_readwrite("colors", &sio::shape::colors)
    .def_readwrite("radius", &sio::shape::radius)
    .def_readwrite("tangents", &sio::shape::tangents);
  
  py::class_<sio::subdiv>(m,"subdiv")
    .def(py::init<std::string, std::vector<vec4i>, std::vector<vec4i>, 
                  std::vector<vec4i>, std::vector<vec3f>, std::vector<vec3f>,
                  std::vector<vec2f>>(),
        // shape data
        py::arg("name") = "",
        // face-varying primitives
        py::arg("quadspos") = std::vector<vec4i>(),
        py::arg("quadsnorm") = std::vector<vec4i>(),
        py::arg("quadstexcoord") = std::vector<vec4i>(),
        // vertex data
        py::arg("positions") = std::vector<vec3f>(),
        py::arg("normals") = std::vector<vec3f>(),
        py::arg("texcoords") = std::vector<vec3f>())
    .def_readwrite("name", &sio::subdiv::name)
    .def_readwrite("quadspos", &sio::subdiv::quadspos)
    .def_readwrite("quadsnorm", &sio::subdiv::quadsnorm)
    .def_readwrite("quadstexcoord", &sio::subdiv::quadstexcoord)
    .def_readwrite("positions", &sio::subdiv::positions)
    .def_readwrite("normals", &sio::subdiv::normals)
    .def_readwrite("texcoords", &sio::subdiv::texcoords);
  
  py::class_<sio::instance>(m, "instance")
    .def(py::init<std::string, std::vector<frame3f>>(),
        py::arg("name") = "",
        py::arg("frames") = std::vector<frame3f>())
    .def_readwrite("name", &sio::instance::name)
    .def_readwrite("frames", &sio::instance::frames);
  
  py::class_<sio::object>(m, "object")
    .def(py::init<std::string, frame3f, sio::shape*, sio::material*, sio::instance*, sio::subdiv*>(),
        py::arg("name") = "",
        py::arg("frame") = identity3x4f,
        py::arg("shape") = py::cast<sio::shape*>(nullptr),
        py::arg("material") = py::cast<sio::material*>(nullptr),
        py::arg("instance") = py::cast<sio::instance*>(nullptr),
        py::arg("subdiv") = py::cast<sio::subdiv*>(nullptr))
    .def_readwrite("name", &sio::object::name)
    .def_readwrite("frame", &sio::object::frame)
    .def_readwrite("shape", &sio::object::shape)
    .def_readwrite("material", &sio::object::material)
    .def_readwrite("instance", &sio::object::instance)
    .def_readwrite("subdiv", &sio::object::subdiv);
  
  py::class_<sio::environment>(m, "environment")
    .def(py::init<std::string, frame3f, vec3f, sio::texture*>(),
        py::arg("name") = "",
        py::arg("frame") = identity3x4f,
        py::arg("emission") = vec3f(0, 0, 0),
        py::arg("emission_tex") = py::cast<sio::texture*>(nullptr))
    .def_readwrite("name", &sio::environment::name)
    .def_readwrite("frame", &sio::environment::frame)
    .def_readwrite("emission" , &sio::environment::emission)
    .def_readwrite("emission_tex", &sio::environment::emission_tex);

  py::class_<sio::model>(m, "model")
    .def(py::init<std::vector<sio::camera*>, std::vector<sio::object*>,
                  std::vector<sio::environment*>, std::vector<sio::shape*>,
                  std::vector<sio::subdiv*>, std::vector<sio::texture*>,
                  std::vector<sio::material*>, std::vector<sio::instance*>,
                  std::string, std::string>(), 
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
    .def("get", []() -> sio::model* {
      auto ioscene_guard =  std::unique_ptr<sio::model>(new sio::model());
      // auto ioscene_guard = std::make_unique<sio::model>().get();
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

  // Load/save a scene in the supported formats. Throws on error.
  m.def("load_scene", &sio::load_scene, py::arg("filename"), py::arg("scene"), py::arg("error"),
      py::arg("progress_cb") = std::function<void(const std::string&, int, int)>(), py::arg("noparallel") = false);
  
  m.def("save_scene", &sio::save_scene, py::arg("filename"), py::arg("scene"), py::arg("error"),
      py::arg("progress_cb") = std::function<void(const std::string&, int, int)>(), py::arg("noparallel") = false);

  // get named camera or default if name is empty
  m.def("get_camera", &sio::get_camera, py::arg("scene"), py::arg("name") = "", py::return_value_policy::reference);
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
  // -----------------------------------------------------------------------------
  // SCENE STATS AND VALIDATION
  // -----------------------------------------------------------------------------
  m.def("scene_stats", &sio::scene_stats, py::arg("scene"), py::arg("verbose") = false);
  m.def("scene_validation",&sio::scene_validation, py::arg("scene"), py::arg("notextures") = false);
  // -----------------------------------------------------------------------------
  // SCENE UTILITIES
  // -----------------------------------------------------------------------------
  m.def("tesselate_subdiv", &sio::tesselate_subdiv, py::arg("scene"), py::arg("subdiv"));
}


// -----------------------------------------------------------------------------
// YOCTO-TRACE
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_trace, m) {

  // const py::object coat_ior = py::cast(trace::coat_ior);
  // m.attr("coat_ior") = coat_ior; 

  // m.def("eval_normal", &trace::eval_normal);

}


// -----------------------------------------------------------------------------
// FYLESYSTEM
// -----------------------------------------------------------------------------
PYBIND11_MODULE(py_filesystem, m) {

  m.def("path_extension", [](std::string imfilename) -> std::string {
    return fs::path(imfilename).extension().string();
  });
  m.def("path_replace_extension", [](std::string imfilename, std::string ext) -> std::string {
    return fs::path(imfilename).replace_extension(ext).string();
  });
  m.def("path_stem", [](std::string filename) -> std::string {
    return fs::path(filename).stem().string();
  });
  m.def("path_exists", [](std::string dirname) -> bool{
    return fs::exists(fs::status(dirname));
  });
  m.def("path_create_directories", [](std::string dirname)-> bool{
    return fs::create_directories(dirname);
  });
  m.def("path_parent_path", [](std::string output)-> std::string{
    return fs::path(output).parent_path();
  });
}
  
}  // namespace yocto::extension