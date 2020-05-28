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
