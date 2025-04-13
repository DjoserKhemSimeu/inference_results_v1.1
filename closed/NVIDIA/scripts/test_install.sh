#!/bin/bash


check_executable() {
    if command -v $1 &> /dev/null; then
        echo "$1 est installé."
    else
        echo "$1 n'est pas installé."
    fi
}


check_version() {
    if command -v $1 &> /dev/null; then
        version=$($1 --version 2>&1 | head -n 1)
        echo "$1 version: $version"
    else
        echo "$1 n'est pas installé."
    fi
}


check_python_module() {
    if python3 -c "import $1" &> /dev/null; then
        version=$(python3 -c "import $1; print($1.__version__)")
        echo "$1 version: $version"
    else
        echo "$1 n'est pas installé."
    fi
}


echo "Vérification des exécutables..."
check_executable python3
check_executable python
check_executable cmake
check_executable gcc
check_executable g++
check_executable nvcc
check_executable git
check_executable virtualenv
check_executable ntpdate
check_executable clang
check_executable make


echo "Vérification des versions des exécutables..."
check_version python3
check_version cmake
check_version gcc
check_version nvcc
check_version git
check_version clang


echo "Vérification des modules Python..."
check_python_module tensorrt
check_python_module numpy
check_python_module scipy
check_python_module matplotlib
check_python_module pycocotools
check_python_module scikit_learn
check_python_module pycuda
check_python_module torch
check_python_module torchvision
check_python_module tensorflow
check_python_module nvidia.dali


echo "Vérification des bibliothèques spécifiques..."
if [ -f /usr/include/aarch64-linux-gnu/cub/cub.cuh ]; then
    echo "CUB est installé."
else
    echo "CUB n'est pas installé."
fi

if [ -f /usr/include/gflags/gflags.h ]; then
    echo "gflags est installé."
else
    echo "gflags n'est pas installé."
fi

if [ -f /usr/include/glog/logging.h ]; then
    echo "glog est installé."
else
    echo "glog n'est pas installé."
fi

echo "Vérification terminée."
