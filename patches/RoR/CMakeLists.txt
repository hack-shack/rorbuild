# ========================================
# Rigs of Rods CMake config file
#
# Description		:		This CMakeLists.txt file sets up the CMake build system
#     				:		for building Rigs of Rods.
# ========================================


# Project setup
# -------------
PROJECT(RoR)
MESSAGE("RoR_SOURCE_DIR: ${RoR_SOURCE_DIR}")
MESSAGE("RoR_BINARY_DIR: ${RoR_BINARY_DIR}")


INCLUDE(CMakeMacros.txt)
# RoR requires CMake policy CMP0003.
CMAKE_MINIMUM_REQUIRED(VERSION 2.6.2)
IF(COMMAND CMAKE_POLICY)
  CMAKE_POLICY(SET CMP0003 NEW)
ENDIF(COMMAND CMAKE_POLICY)

# Build configurations
# --------------------
SET(CMAKE_CONFIGURATION_TYPES "RelWithDebInfo;Release" CACHE STRING "" FORCE)


# Platform-specific configuration
# -------------------------------
IF(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
	SET(CMAKE_GENERATOR "Xcode")
	SET(BUILD_TARGET "osx_10.9")
	MESSAGE(STATUS "TARGET         :  ${BUILD_TARGET}")
	MESSAGE(STATUS "GENERATOR      :  ${CMAKE_GENERATOR}")
	MESSAGE(STATUS "CONFIGURATIONS :  ${PLATFORMS}")
	MESSAGE(STATUS "ARCHITECTURE   :  ${ARCH_DIR}")
	MESSAGE(STATUS "CMAKE_CL_64    :  ${CMAKE_CL_64}")
ENDIF()

IF(WIN32)
	SET(arch_dir "")
	MESSAGE(STATUS "cmake_generator: ${cmake_generator}")
	MESSAGE(STATUS "cmake_cl_64: ${cmake_cl_64}")
	IF(cmake_cl_64) 
		SET(arch_dir "x64") 
		MESSAGE(STATUS "Using 64 bit libraries.")
	ELSE() 
		SET(arch_dir "x86") 
		MESSAGE(STATUS "Using 32 bit libraries.")
	ENDIF() 
ENDIF()



# Setup the default build mode
# ---------------------------- 
SET(BUILD_SHARED_LIBS ON)
SET(CMAKE_USE_RELATIVE_PATHS OFF)
SET(RoR_DEPENDENCY_DIR       "${RoR_SOURCE_DIR}/dependencies_0.4.0.7_osx_10.9")


# Define output directories for the executable, libraries, and object files.
SET(RUNTIME_OUTPUT_DIRECTORY "${RoR_SOURCE_DIR}/bin/")
SET(LIBRARY_OUTPUT_DIRECTORY "${RoR_SOURCE_DIR}/cmake_lib/")
SET(ARCHIVE_OUTPUT_DIRECTORY "${RoR_SOURCE_DIR}/cmake_lib/")
SET(RoR_Dependencies_CMAKE_DIR "${RoR_DEPENDENCY_DIR}/cmake")


# set the tools binary directory for current platform
IF(WIN32)
  SET(ROR_BINTOOL_DIR             ${RoR_SOURCE_DIR}/tools/windows/binaries)
ELSEIF(UNIX)
  SET(ROR_BINTOOL_DIR             ${RoR_SOURCE_DIR}/tools/linux/binaries)
ELSEIF(APPLE)
  SET(ROR_BINTOOL_DIR             ${RoR_SOURCE_DIR}/tools/osx/binaries)
ENDIF(WIN32)

SET(CMAKE_DEBUG_POSTFIX _d)

# hide some settings
MARK_AS_ADVANCED(
  CMAKE_DEBUG_POSTFIX
  CMAKE_BACKWARDS_COMPATIBILITY
  Boost_LIB_DIAGNOSTIC_DEFINITIONS
)

#  Windows
#  ----------------------------------------------------------------------------
IF(WIN32)
  #SET(ROR_USING_VISUAL_STUDIO_PROFESSIONAL "FALSE" CACHE BOOL "if you use VS professional, enable this. DO NOT enable this when using express versions")

# Disable annoying warnings in Visual Studio Express 2008
  SET(warnings /W3 /D_CRT_SECURE_NO_WARNINGS /wd4005 /wd4996 /wd4251 /wd4275 /wd4099 /nologo)
  add_definitions(${warnings})

# Flags for Release build configuration
# MP: enable parallel builds
# GL: enable "whole program optimization" in Visual Studio
  SET(CMAKE_CXX_FLAGS_RELEASE        "${CMAKE_CXX_FLAGS_RELEASE}        /MP /GL /Ox /Ob2 /Oi /Ot /Oy /fp:fast /GS- /MP /Zi")
  SET(CMAKE_CXX_FLAGS_MINSIZEREL     "${CMAKE_CXX_FLAGS_MINSIZEREL}     /MP /Zi")
  SET(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} /MP /Od /Zi /Gy /fp:except /GF- /GS /Ob0")
  # Visual Studio Professional supports the /analyze switch
  #IF(ROR_USING_VISUAL_STUDIO_PROFESSIONAL)
  #  SET(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} /analyze")
  #ENDIF(ROR_USING_VISUAL_STUDIO_PROFESSIONAL)
  SET(CMAKE_CXX_FLAGS_DEBUG          "${CMAKE_CXX_FLAGS_DEBUG}          /MP /Od /Zi /RTC1 /Gy /fp:except /GF- /RTCc /GS /Ob0")
  # Disable C4996 warnings using secure CRT functions
  add_definitions("-D_CRT_SECURE_NO_WARNINGS")
  
  include_directories(${DirectX_INCLUDE_DIR})

  SET(CMAKE_EXE_LINKER_FLAGS_DEBUG          "${CMAKE_EXE_LINKER_FLAGS_DEBUG}          /DEBUG /LARGEADDRESSAWARE ")
  SET(CMAKE_EXE_LINKER_FLAGS_RELEASE        "${CMAKE_EXE_LINKER_FLAGS_RELEASE}        /DEBUG /LARGEADDRESSAWARE /OPT:REF /LTCG /RELEASE")
  SET(CMAKE_EXE_LINKER_FLAGS_MINSIZEREL     "${CMAKE_EXE_LINKER_FLAGS_MINSIZEREL}     /DEBUG /LARGEADDRESSAWARE /OPT:REF /LTCG ")
  SET(CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO "${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO} /DEBUG /LARGEADDRESSAWARE /OPT:NOREF /MAP /DYNAMICBASE:NO /FIXED /NXCOMPAT:NO")

	# fix executable paths for windows
	#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${RUNTIME_OUTPUT_DIRECTORY})
	#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${RUNTIME_OUTPUT_DIRECTORY})
	#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO ${RUNTIME_OUTPUT_DIRECTORY})
	#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${RUNTIME_OUTPUT_DIRECTORY})


# Linux
# -----------------------------------------------------------------------------
ELSEIF(UNIX)
  SET(CMAKE_EXE_LINKER_FLAGS_DEBUG          "${CMAKE_EXE_LINKER_FLAGS_DEBUG}          -O0 -ggdb")
  SET(CMAKE_EXE_LINKER_FLAGS_RELEASE        "${CMAKE_EXE_LINKER_FLAGS_RELEASE}        -mfpmath=sse -msse2 -mmmx -msse -msse3 -m3dnow -O2 -fomit-frame-pointer -fstrict-aliasing -ffast-math -ftracer")
  SET(CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO "${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO} -O0")

  # add additional gdb debugging stuff
  SET(CMAKE_SHARED_LINKER_FLAGS_DEBUG       "${CMAKE_SHARED_LINKER_FLAGS_DEBUG} -O0 -ggdb")
  SET(CMAKE_MODULE_LINKER_FLAGS_DEBUG       "${CMAKE_MODULE_LINKER_FLAGS_DEBUG} -O0 -ggdb")


# OS X
# -----------------------------------------------------------------------------
ELSEIF(APPLE)
  SET(CMAKE_CXX_FLAGS "--sysroot ${CMAKE_OSX_SYSROOT} ${CMAKE_CXX_FLAGS}")
  SET(CMAKE_EXE_LINKER_FLAGS_DEBUG" ${CMAKE_EXE_LINKER_FLAGS_DEBUG} -O0 -ggdb")
  SET(CMAKE_EXE_LINKER_FLAGS_RELEASE" ${CMAKE_EXE_LINKER_FLAGS_RELEASE} -mfpmath=sse -msse2 -mmmx -msse -msse3 -m3dnow -O2 -fomit-frame-pointer -fstrict-aliasing -ffast-math -ftracer")
  SET(CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO"${CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO} -O0")

  # add additional gdb debugging stuff
  SET(CMAKE_SHARED_LINKER_FLAGS_DEBUG"${CMAKE_SHARED_LINKER_FLAGS_DEBUG} -O0 -ggdb")
  SET(CMAKE_MODULE_LINKER_FLAGS_DEBUG       "${CMAKE_MODULE_LINKER_FLAGS_DEBUG} -O0 -ggdb")
ENDIF(WIN32)

INCLUDE(CMakeDependenciesConfig.txt)


# Add the "source" directory:
#   * RoR itself (in the directory named "main")
#   * RoR Configurator
#   * AngelScript addons.
ADD_SUBDIRECTORY(source)