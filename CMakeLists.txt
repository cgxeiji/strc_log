add_library(cgx_strc_log INTERFACE)

target_include_directories(cgx_strc_log INTERFACE .)

if (not TARGET cgx_strc)
    add_library(./libs/strc)
endif()

add_subdirectory(./include/strc_log)
add_dependencies(cgx_strc_log cgx_strc)
