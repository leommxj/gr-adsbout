INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ADSBOUT adsbout)

FIND_PATH(
    ADSBOUT_INCLUDE_DIRS
    NAMES adsbout/api.h
    HINTS $ENV{ADSBOUT_DIR}/include
        ${PC_ADSBOUT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ADSBOUT_LIBRARIES
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

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ADSBOUT DEFAULT_MSG ADSBOUT_LIBRARIES ADSBOUT_INCLUDE_DIRS)
MARK_AS_ADVANCED(ADSBOUT_LIBRARIES ADSBOUT_INCLUDE_DIRS)

