cmake_minimum_required (VERSION 3.12)
cmake_policy(SET CMP0079 NEW)

project (yocto_pathextension VERSION 2.0)

# find_package(pybind11)
# find_package(PythonInterp)
# find_package(PythonLibs)

# GCC/clang:
set(PYBIND11_CPP_STANDARD -std=c++1z) # Experimental C++17 support
add_subdirectory(libs/pybind11) 
# pybind11_add_module(test_yscene libs/yocto/yocto_trace.cpp)
# pybind11_add_module(example libs/yocto/yocto_trace.cpp)
pybind11_add_module(py_pathtrace libs/yocto_extension/yocto_extension.cpp)
pybind11_add_module(py_commonio libs/yocto_extension/yocto_extension.cpp)
pybind11_add_module(py_sceneio libs/yocto_extension/yocto_extension.cpp)


option(YOCTO_OPENGL "Build OpenGL apps" ON)
option(YOCTO_EMBREE "Use Intel's Embree raytracer" OFF)
option(YOCTO_TESTING "Enable testing" OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE "RelWithDebInfo")
endif()

set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin)
if(NOT GENERATOR_IS_MULTI_CONFIG AND CMAKE_BUILD_TYPE MATCHES Debug)
  set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin/debug)
endif(NOT GENERATOR_IS_MULTI_CONFIG AND CMAKE_BUILD_TYPE MATCHES Debug)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
if(GENERATOR_IS_MULTI_CONFIG)
  set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR})
  set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR})
  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR})
endif(GENERATOR_IS_MULTI_CONFIG)

# platform compile flags
if(APPLE)
  add_definitions(-Wall)
endif(APPLE)
if(MSVC)
  add_definitions(/D_CRT_SECURE_NO_WARNINGS /wd4018 /wd4244 /wd4305 /wd4800 /wd4267)
  set(CMAKE_CXX_FLAGS "/EHsc")
endif(MSVC)

add_subdirectory(libs)
add_subdirectory(apps)


# find_package(pybind11 REQUIRED)
# target_link_libraries(test_yscene PRIVATE yocto)
# set_target_properties(yocto PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
# target_link_libraries(test_yscene PUBLIC yocto)
# pybind11_add_module(py_pathtrace SHARED libs/yocto_pathtrace/yocto_pathtrace.cpp)
# target_include_directories(py_pathtrace PUBLIC libs)
# set_target_properties(yocto PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
# target_link_libraries(py_pathtrace PRIVATE yocto)