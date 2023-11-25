add_library(cgx_strc_log INTERFACE)

target_include_directories(cgx_strc_log INTERFACE .)

if (NOT TARGET cgx_strc)
    add_subdirectory(./libs/strc)
endif()

add_dependencies(cgx_strc_log cgx_strc)
