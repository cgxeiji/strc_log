project(example_logger)
cmake_minimum_required(VERSION 3.13)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -Wextra -Werror -ffile-prefix-map=${CMAKE_SOURCE_DIR}/=/ -fmacro-prefix-map=${CMAKE_SOURCE_DIR}/=/")

add_executable(example_logger main.cpp)

set_property(TARGET example_logger PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)

target_sources(example_logger PRIVATE
    ./strc.cpp
)

