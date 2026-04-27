cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(inference-server)

macro(use_cxx11)
  if (CMAKE_VERSION VERSION_LESS "3.1")
    if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
    endif ()
  else ()
    set (CMAKE_CXX_STANDARD 17)
  endif ()
endmacro(use_cxx11)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -fexceptions")

find_path(MSGPACK_INCLUDE_DIR msgpack.hpp)

set(SOURCES src/main.cpp src/postprocess.cpp src/rk_common.cpp)

set(EXTRA_LIBS /usr/local/lib/librknnrt.so )

set(EXECUTABLE_OUTPUT_PATH "../")

include_directories(include ${MSGPACK_INCLUDE_DIR})

add_link_options(-fopenmp -s -ldl -lpthread -pthread -lgomp -rdynamic -march=armv8.2-a)

add_executable(inference-server ${SOURCES})

target_link_libraries(inference-server ${EXTRA_LIBS})
