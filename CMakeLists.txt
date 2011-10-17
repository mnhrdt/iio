cmake_minimum_required (VERSION 2.6) #specify the required version of cmake
project (IIO)                        #give a name to the project/solution

# ADD LOCAL PATH TO SEARCH MODULES
LIST(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_PREFIX}")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR})


SET (LIBS "")


# IF AVAILABLE USE OPENEXR
FIND_PACKAGE(OPENEXR) 
# OPENEXR_FOUND = OpenEXR found. 
# OPENEXR_INCLUDE_PATHS = OpenEXR include directories.
# OPENEXR_LIBRARIES = libraries that are needed to use OpenEXR.
IF (OPENEXR_FOUND) 
  include_directories(${OPENEXR_INCLUDE_PATHS})
  SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DI_CAN_HAS_LIBEXR")
  SET( LIBS ${LIBS} ${OPENEXR_LIBRARIES})
ENDIF()

# OTHER LIBRARIES
find_package(TIFF)
if(TIFF_FOUND)
  include_directories(${TIFF_INCLUDE_DIR})
  #  link_directories(${TIFF_LIBRARY})
  SET( LIBS ${LIBS} ${TIFF_LIBRARIES})
ENDIF()

find_package(JPEG)
if(JPEG_FOUND)
  include_directories(${JPEG_INCLUDE_DIR})
  # link_directories(${JPEG_LIBRARY})
  SET( LIBS ${LIBS} ${JPEG_LIBRARIES})
ENDIF()

find_package(PNG)
if(PNG_FOUND)
  include_directories(${PNG_INCLUDE_DIR})
  #  link_directories(${PNG_LIBRARY})
  SET( LIBS ${LIBS} ${PNG_LIBRARIES})
ENDIF()


# IIO
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -std=c99 -funroll-loops -Wno-unused")
MESSAGE( "FLAGS: ${CMAKE_C_FLAGS}")
SET(IIO_LIB_SRCS iio.h iio.c)       #Define a variable that contains files of the lib
ADD_LIBRARY(IIOLIB ${IIO_LIB_SRCS}) #Define that those files create the lib FooLib


# EXAMPLE
add_executable (iio iio_test.c)
target_link_libraries(iio IIOLIB ${LIBS})

add_executable (iion iio_test_named.c)
target_link_libraries(iion IIOLIB ${LIBS})


##setup Config.cmake
SET(PARAMETROS_BASE_DIR "${PROJECT_SOURCE_DIR}")
set(PARAMETROS_CMAKE_DIR "${PROJECT_BINARY_DIR}")
set(IIO_LIBS ${LIBS} ${PROJECT_SOURCE_DIR}/libIIOLIB.a)
set(IIO_INCLUDE ${PROJECT_SOURCE_DIR})
MESSAGE( "${PROJECT_BINARY_DIR}" )
MESSAGE( "${PROJECT_SOURCE_DIR}" )
configure_file(iioConfig.cmake.in
     "${PROJECT_BINARY_DIR}/iioConfig.cmake" @ONLY)

