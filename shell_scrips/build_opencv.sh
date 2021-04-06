#!/bin/bash

# Parse flags
while test $# -gt 0; do
    case "$1" in
        -opencv_version)
            shift && OPENCV_VERSION=$1 && shift;;
        -cuda_version)
            shift && CUDA_VERSION=$1 && shift;;
        -gcc_version)
            shift && GCC_VERSION=$1 && shift;;
        -python3_include_dir)
            shift && PYTHON3_INCLUDE_DIR=$1 && shift;;
        -python3_packages_path)
            shift && PYTHON3_PACKAGES_PATH=$1 && shift;;
        -python3_library)
            shift && PYTHON3_LIBRARY=$1 && shift;;
        *)
            echo "Error: unexpected flag ($1)"
            exit 1
    esac
done

# Required flags
if [ -z "$PYTHON3_INCLUDE_DIR" ]; then
    echo "Error: python3_include_dir is required" && exit 1
else
    echo "PYTHON3_INCLUDE_DIR=$PYTHON3_INCLUDE_DIR"
fi
if [ -z "$PYTHON3_PACKAGES_PATH" ]; then
    echo "Error: python3_packages_path is required" && exit 1
else
    echo "PYTHON3_PACKAGES_PATH=$PYTHON3_PACKAGES_PATH"
fi
if [ -z "$PYTHON3_LIBRARY" ]; then
    echo "Error: python3_library is required" && exit 1
else
    echo "PYTHON3_LIBRARY=$PYTHON3_LIBRARY"
fi

# Optional flags
if [ -z "$OPENCV_VERSION" ]; then
    OPENCV_VERSION=4.4.0
fi
if [ -z "$CUDA_VERSION" ]; then
    CUDA_VERSION=10.1
fi
if [ -z "$GCC_VERSION" ]; then
    GCC_VERSION=7
fi
echo "OPENCV_VERSION=$OPENCV_VERSION"
echo "CUDA_VERSION=$CUDA_VERSION"
echo "GCC_VERSION=$GCC_VERSION"

mkdir opencv
cd opencv

wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip
unzip opencv.zip
unzip opencv_contrib.zip

cd opencv-$OPENCV_VERSION

mkdir build
cd build

cmake \
-D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
-D PYTHON_EXECUTABLE=$(which python) \
-D PYTHON3_EXECUTABLE=$(which python3) \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D BUILD_opencv_python3=ON \
-D BUILD_opencv_python2=OFF \
-D BUILD_PACKAGE=ON \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D WITH_CUDA=ON \
-D WITH_CUFFT=ON \
-D WITH_CUBLAS=ON \
-D WITH_TBB=ON \
-D WITH_IPP=ON \
-D OPENCV_DNN_CUDA=ON \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D ENABLE_FAST_MATH=1 \
-D CUDA_FAST_MATH=1 \
-D CMAKE_C_COMPILER=/usr/bin/gcc-$GCC_VERSION \
-D CMAKE_CXX_COMPILER=/usr/bin/g++-$GCC_VERSION \
-D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-$CUDA_VERSION \
-D PYTHON3_INCLUDE_DIR=$PYTHON3_INCLUDE_DIR \
-D PYTHON3_PACKAGES_PATH=$PYTHON3_PACKAGES_PATH \
-D PYTHON3_NUMPY_INCLUDE_DIRS=$PYTHON3_PACKAGES_PATH/numpy/core/include \
-D PYTHON3_LIBRARY=$PYTHON3_LIBRARY \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-$OPENCV_VERSION/modules \
..

make -j$(nproc --all)
make install
ldconfig -v

rm -rf opencv