#!/bin/sh
nasm -felf64 $1 -o build.o && ld build.o && rm build.o && ./a.out
