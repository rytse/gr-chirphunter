INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_CHIRPHUNTER chirphunter)

FIND_PATH(
    CHIRPHUNTER_INCLUDE_DIRS
    NAMES chirphunter/api.h
    HINTS $ENV{CHIRPHUNTER_DIR}/include
        ${PC_CHIRPHUNTER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    CHIRPHUNTER_LIBRARIES
    NAMES gnuradio-chirphunter
    HINTS $ENV{CHIRPHUNTER_DIR}/lib
        ${PC_CHIRPHUNTER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/chirphunterTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CHIRPHUNTER DEFAULT_MSG CHIRPHUNTER_LIBRARIES CHIRPHUNTER_INCLUDE_DIRS)
MARK_AS_ADVANCED(CHIRPHUNTER_LIBRARIES CHIRPHUNTER_INCLUDE_DIRS)
