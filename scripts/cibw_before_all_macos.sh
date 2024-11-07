#!/bin/bash
set -e -x

brew install gcc
make CXX=g++-14 CC=gcc-14
ln -sf /usr/local/bin/gcc-14 /usr/local/bin/gcc
gcc --version
