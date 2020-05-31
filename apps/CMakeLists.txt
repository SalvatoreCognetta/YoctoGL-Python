add_subdirectory(yscenetrace)
add_subdirectory(ysceneproc)
add_subdirectory(yimageproc)
add_subdirectory(yshapeproc)

if(YOCTO_OPENGL)
add_subdirectory(ysceneitraces)
endif(YOCTO_OPENGL)
