add_library(yocto_extension yocto_extension.h yocto_extension.cpp)

set_target_properties(yocto_extension PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES)
target_include_directories(yocto_extension PUBLIC ${CMAKE_SOURCE_DIR}/libs)
target_link_libraries(yocto_extension yocto yocto_pathtrace)

# pybind11
# target_include_directories(py_math PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_math PRIVATE yocto yocto_pathtrace) # https://github.com/pybind/pybind11/issues/387

# target_include_directories(py_shape PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_shape PRIVATE yocto yocto_pathtrace)

target_include_directories(py_image PUBLIC ${CMAKE_SOURCE_DIR}/libs)
target_link_libraries(py_image PRIVATE yocto yocto_pathtrace)

# target_include_directories(py_pathtrace PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_pathtrace PRIVATE yocto yocto_pathtrace)


# target_include_directories(py_commonio PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_commonio PRIVATE yocto yocto_pathtrace)


# target_include_directories(py_sceneio PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_sceneio PRIVATE yocto yocto_pathtrace)


# target_include_directories(py_trace PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_trace PRIVATE yocto yocto_pathtrace)


# target_include_directories(py_filesystem PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(py_filesystem PRIVATE yocto)