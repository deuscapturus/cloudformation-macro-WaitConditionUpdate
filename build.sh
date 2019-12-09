#!/bin/bash
cd "$(dirname "$0")"

mkdir -p build
rm -rf build/*
cp -rp ./src/* build/

#pip3 install -r requirements.txt -t build
