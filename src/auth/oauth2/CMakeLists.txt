# OAuth 2 Authentication Method plugin

########################################################
# Packages

if(WITH_VGPKG)
  set(WITH_INTERNAL_O2_DEFAULT OFF)
else()
  set(WITH_INTERNAL_O2_DEFAULT ON)
endif()
option(WITH_INTERNAL_O2 "Download and locally include source of o2 library" ${WITH_INTERNAL_O2_DEFAULT})

if(WITH_INTERNAL_O2)
  set(O2_SOURCE_DIR ${CMAKE_SOURCE_DIR}/external/o2/src)
  set(O2_INCLUDE_DIR "${O2_SOURCE_DIR}" CACHE INTERNAL "Path to o2 library headers" FORCE)
  set(O2_LIBRARY "" CACHE INTERNAL "Path to o2 built shared library" FORCE)
  set(O2_LIBRARY_STATIC "" CACHE INTERNAL "Path to o2 built static library" FORCE)
  set(O2_FOUND TRUE CACHE INTERNAL "Whether O2 has been found" FORCE)
else()
  find_package(O2 REQUIRED)
endif()

if(WITH_INTERNAL_O2)
  set(O2_SRCS
    ${O2_SOURCE_DIR}/o0baseauth.cpp
    ${O2_SOURCE_DIR}/o0jsonresponse.cpp
    ${O2_SOURCE_DIR}/o0keychainstore.cpp
    ${O2_SOURCE_DIR}/o0settingsstore.cpp
    ${O2_SOURCE_DIR}/o2.cpp
    ${O2_SOURCE_DIR}/o2pollserver.cpp
    ${O2_SOURCE_DIR}/o2reply.cpp
    ${O2_SOURCE_DIR}/o2replyserver.cpp
    ${O2_SOURCE_DIR}/o2requestor.cpp
    ${O2_SOURCE_DIR}/o2simplecrypt.cpp
  )
  set(O2_HDRS
    ${O2_INCLUDE_DIR}/o0abstractstore.h
    ${O2_INCLUDE_DIR}/o0jsonresponse.h
    ${O2_INCLUDE_DIR}/o0baseauth.h
    ${O2_INCLUDE_DIR}/o0export.h
    ${O2_INCLUDE_DIR}/o0globals.h
    ${O2_INCLUDE_DIR}/o0keychainstore.h
    ${O2_INCLUDE_DIR}/o2pollserver.h
    ${O2_INCLUDE_DIR}/o0requestparameter.h
    ${O2_INCLUDE_DIR}/o0settingsstore.h
    ${O2_INCLUDE_DIR}/o0simplecrypt.h
    ${O2_INCLUDE_DIR}/o2.h
    ${O2_INCLUDE_DIR}/o2reply.h
    ${O2_INCLUDE_DIR}/o2replyserver.h
    ${O2_INCLUDE_DIR}/o2requestor.h
  )
endif()

########################################################
# Source files
set(AUTH_OAUTH2_SRCS
  core/qgso2.cpp
  core/qgsauthoauth2config.cpp
  core/qgsauthoauth2method.cpp
)

set(AUTH_OAUTH2_HDRS
  core/qgsauthoauth2config.h
  core/qgsauthoauth2method.h
  core/qgso2.h
)

if(WITH_INTERNAL_O2)
  set(AUTH_OAUTH2_HDRS ${AUTH_OAUTH2_HDRS} ${O2_HDRS})
  set(AUTH_OAUTH2_SRCS ${AUTH_OAUTH2_SRCS} ${O2_SRCS})
endif()

set(AUTH_OAUTH2_RCCS resources/oauth2_resources.qrc)

set(AUTH_OAUTH2_UIS_H "")

if (WITH_GUI)
  set(AUTH_OAUTH2_SRCS ${AUTH_OAUTH2_SRCS}
    gui/qgsauthoauth2edit.cpp
  )

  set(AUTH_OAUTH2_HDRS ${AUTH_OAUTH2_HDRS}
    gui/qgsauthoauth2edit.h
  )

  set(AUTH_OAUTH2_UIS gui/qgsauthoauth2edit.ui)
  qt_wrap_ui(AUTH_OAUTH2_UIS_H ${AUTH_OAUTH2_UIS})
  
endif()

############################################################
# Generate files
if(WITH_INTERNAL_O2 AND CMAKE_GENERATOR MATCHES "Ninja")
  # handle `cmake --help-policy CMP0058`
  #  "Ninja requires custom command byproducts to be explicit,"
  #   which the downloaded o2 source files are not. Add phony command target...
  add_custom_command(
    OUTPUT ${O2_HDRS}
    COMMAND
  )
endif()

# static library
add_library(authmethod_oauth2_a STATIC ${AUTH_OAUTH2_SRCS} ${AUTH_OAUTH2_HDRS} ${AUTH_OAUTH2_RCCS} ${AUTH_OAUTH2_UIS_H})

target_include_directories(authmethod_oauth2_a PUBLIC ${CMAKE_SOURCE_DIR}/src/auth/oauth2/core)

# require c++17
target_compile_features(authmethod_oauth2_a PRIVATE cxx_std_17)
target_compile_definitions(authmethod_oauth2_a PRIVATE "CMAKE_SOURCE_DIR=\"${CMAKE_SOURCE_DIR}\"")

target_link_libraries(authmethod_oauth2_a qgis_core)

if(WITH_INTERNAL_O2)
  target_include_directories(authmethod_oauth2_a SYSTEM PUBLIC ${O2_INCLUDE_DIR})
else()
  target_link_libraries(authmethod_oauth2_a o2::o2)
endif()

target_include_directories(authmethod_oauth2_a PRIVATE
  ${CMAKE_SOURCE_DIR}/src/auth/oauth2/core
)
if (WITH_GUI)
  target_include_directories(authmethod_oauth2_a PRIVATE
    ${CMAKE_SOURCE_DIR}/src/auth/oauth2/gui
    ${CMAKE_BINARY_DIR}/src/auth/oauth2
  )
  target_link_libraries (authmethod_oauth2_a qgis_gui)
endif()



if (FORCE_STATIC_LIBS)
  # for (external) mobile apps to be able to pick up provider for linking
  install (TARGETS authmethod_oauth2_a ARCHIVE DESTINATION ${QGIS_PLUGIN_DIR})
else()
  # dynamically loaded module
  add_library(authmethod_oauth2 MODULE ${AUTH_OAUTH2_SRCS} ${AUTH_OAUTH2_HDRS} ${AUTH_OAUTH2_RCCS} ${AUTH_OAUTH2_UIS_H})

  target_include_directories(authmethod_oauth2 PRIVATE
    ${CMAKE_SOURCE_DIR}/src/auth/oauth2/core
  )

  # require c++17
  target_compile_features(authmethod_oauth2 PRIVATE cxx_std_17)
  target_compile_definitions(authmethod_oauth2 PRIVATE "CMAKE_SOURCE_DIR=\"${CMAKE_SOURCE_DIR}\"")

  target_link_libraries(authmethod_oauth2 qgis_core)

  if(WITH_INTERNAL_O2)
    target_include_directories(authmethod_oauth2 SYSTEM PUBLIC ${O2_INCLUDE_DIR})
  else()
    target_link_libraries(authmethod_oauth2 o2::o2)
  endif()

  if(WIN32)
     add_definitions(-DO2_DLL_EXPORT)
   endif()

  if (WITH_GUI)
    target_include_directories(authmethod_oauth2 PRIVATE
      ${CMAKE_SOURCE_DIR}/src/auth/oauth2/gui
      ${CMAKE_BINARY_DIR}/src/auth/oauth2
    )
    target_link_libraries (authmethod_oauth2 qgis_gui)
    add_dependencies(authmethod_oauth2 ui)
  endif()

  install (TARGETS authmethod_oauth2
    RUNTIME DESTINATION ${QGIS_PLUGIN_DIR}
    LIBRARY DESTINATION ${QGIS_PLUGIN_DIR}
  )
endif()
