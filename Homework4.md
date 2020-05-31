# Installation
On linux:
```bash
sudo apt install pybind11-dev
```

Follow the guide of the official repository for the requirements: https://github.com/pybind/pybind11

# Include pybind lib
Clone the repo inside libs folder and add submodule:
```bash
git submodule add https://github.com/pybind/pybind11
git submodule init
git submodule update
```
https://github.com/pybind/pybind11/issues/1817

# Install correctly pybind11
```bash
cd pybind11
mkdir build
cd build
cmake ..
make install
```

# How to create a module
1. Insert the pybindmodule in the principal cmakelists.txt, and the libs in the cmakelist of yoctoextension (otherwise it will blow up)

## Cmake changes
To allow
```
CMake Error at libs/yocto_extension/CMakeLists.txt:13 (target_link_libraries):
      Attempt to add link library "yocto" to target "py_commonio" which is not
      built in this directory.
    
      This is allowed only when policy CMP0079 is set to NEW.
```
we have setted:
`cmake_policy(SET CMP0079 NEW)`  
See: [link to issue](https://gitlab.kitware.com/cmake/cmake/issues/19693)

# Error with parce_cli and model
Due to the error shown below:
![Core dumped error](report/img/error_parce_cli.png)
we had to create a workaround by creating a simplified parce_cli in python.
Main problem is in "*(std::string*)option.value = value; //*(std::string*) create the problem" inside 
"inline bool parse_cli(cli_state& cli, int argc, const char** argv, std::string& error)"; it looks like it cant convert the object into an std::string pointer.


# Error with yocto_sceneio
To avoid the error below, while creating a new module for yocto_sceneio:  
![Error yocto_sceneio](report/img/error_yoctosceneio.png)  
we had to include all the yocto cpp file:  
![Error yocto_sceneio](report/img/solved_error_yoctosceneio.png)  

# How to build yocto
```bash
pip install . --no-cache-dir
```