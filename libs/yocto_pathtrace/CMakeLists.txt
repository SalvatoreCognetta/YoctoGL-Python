add_library(yocto_pathtrace yocto_pathtrace.h yocto_pathtrace.cpp)

set_target_properties(yocto_pathtrace PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES)
target_include_directories(yocto_pathtrace PUBLIC ${CMAKE_SOURCE_DIR}/libs)
target_link_libraries(yocto_pathtrace yocto)

# pybind11_add_module(py_pathtrace SHARED yocto_pathtrace.cpp)
# target_include_directories(py_pathtrace PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# set_target_properties(py_pathtrace PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES)

# # set_target_properties(yocto PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
# target_link_libraries(py_pathtrace PRIVATE yocto)
