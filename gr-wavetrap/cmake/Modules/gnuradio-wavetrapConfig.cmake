find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_WAVETRAP gnuradio-wavetrap)

FIND_PATH(
    GR_WAVETRAP_INCLUDE_DIRS
    NAMES gnuradio/wavetrap/api.h
    HINTS $ENV{WAVETRAP_DIR}/include
        ${PC_WAVETRAP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_WAVETRAP_LIBRARIES
    NAMES gnuradio-wavetrap
    HINTS $ENV{WAVETRAP_DIR}/lib
        ${PC_WAVETRAP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-wavetrapTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_WAVETRAP DEFAULT_MSG GR_WAVETRAP_LIBRARIES GR_WAVETRAP_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_WAVETRAP_LIBRARIES GR_WAVETRAP_INCLUDE_DIRS)
