add_executable(yscenetrace yscenetrace.cpp)

set_target_properties(yscenetrace PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES)
target_include_directories(yscenetrace PUBLIC ${CMAKE_SOURCE_DIR}/libs)
target_link_libraries(yscenetrace yocto yocto_pathtrace)

# add_subdirectory(../../libs/pybind11) 
# add_executable(test test.cpp)
# target_link_libraries(test_yscene yocto)

# set_target_properties(test PROPERTIES CXX_STANDARD 17 CXX_STANDARD_REQUIRED YES)
# target_include_directories(test PUBLIC ${CMAKE_SOURCE_DIR}/libs)
# target_link_libraries(test yocto)