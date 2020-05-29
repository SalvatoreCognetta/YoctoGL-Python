//
// # Yocto/Extension: Tiny Yocto/GL extension
//
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
//

#ifndef _YOCTO_EXTENSION_H_
#define _YOCTO_EXTENSION_H_

// -----------------------------------------------------------------------------
// INCLUDES
// -----------------------------------------------------------------------------

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <yocto/yocto_commonio.h>
#include <yocto/yocto_image.h>
#include <yocto/yocto_image.cpp>
#include <yocto/ext/stb_image.h>
#include <yocto/ext/stb_image.cpp>

// #include <yocto/yocto_sceneio.h>
#include <yocto/yocto_sceneio.cpp>
#include <yocto/yocto_trace.h>
// #include <yocto/yocto_trace.cpp>
// #include <yocto/ext/cgltf.h>
#include <yocto/ext/cgltf.cpp>
// #include <yocto/ext/tinyexr.h>
#include <yocto/ext/tinyexr.cpp>

#include <yocto/yocto_shape.h>
#include <yocto/yocto_shape.cpp>

#include <yocto/yocto_math.h>


#include <yocto_pathtrace/yocto_pathtrace.h>

#include <atomic>
#include <future>
#include <memory>

// -----------------------------------------------------------------------------
// ALIASES
// -----------------------------------------------------------------------------
namespace yocto::extension {

// Namespace aliases
namespace ext = yocto::extension;
namespace img = yocto::image;
namespace ptr = yocto::pathtrace;
namespace cli = yocto::commonio;
namespace sio = yocto::sceneio;
namespace trace = yocto::trace;

// Math defitions
using math::bbox3f;
using math::byte;
using math::frame3f;
using math::identity3x4f;
using math::ray3f;
using math::rng_state;
using math::vec2f;
using math::vec2i;
using math::vec3b;
using math::vec3f;
using math::vec3i;
using math::vec4f;
using math::vec4i;
using math::zero2f;
using math::zero3f;

}  // namespace yocto::pathtrace

// -----------------------------------------------------------------------------
// HIGH LEVEL API
// -----------------------------------------------------------------------------
namespace yocto::extension {

}  // namespace yocto::pathtrace

#endif
