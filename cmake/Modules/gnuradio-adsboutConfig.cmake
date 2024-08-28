find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_ADSBOUT gnuradio-adsbout)

FIND_PATH(
    GR_ADSBOUT_INCLUDE_DIRS
    NAMES gnuradio/adsbout/api.h
    HINTS $ENV{ADSBOUT_DIR}/include
        ${PC_ADSBOUT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_ADSBOUT_LIBRARIES
    NAMES gnuradio-adsbout
    HINTS $ENV{ADSBOUT_DIR}/lib
        ${PC_ADSBOUT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-adsboutTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_ADSBOUT DEFAULT_MSG GR_ADSBOUT_LIBRARIES GR_ADSBOUT_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_ADSBOUT_LIBRARIES GR_ADSBOUT_INCLUDE_DIRS)
