cmake_minimum_required(VERSION 3.28)
project(pps C)

set(CMAKE_C_STANDARD 11)

include_directories(.)
include_directories(extra)

add_executable(pps
        extra/binary_to_decimal.c
        extra/decimal_to_any.c
        extra/decimal_to_binary.c
        assignment10_calendar.c
        assignment3_calculator.c
        assignment4_matrices.c
        assignment5_strings.c
        assignment6_factorial.c
        assignment7_structs.c
        assignment8_swap.c
        assignment9_filehandling.c
        library_management.c)
