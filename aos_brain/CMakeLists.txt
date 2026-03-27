cmake_minimum_required(VERSION 3.14)
project(aos_brain VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find packages
find_package(Threads REQUIRED)
find_package(nlohmann_json 3.2.0 REQUIRED)

# If nlohmann_json not found via find_package, use bundled version
if(NOT nlohmann_json_FOUND)
    include(FetchContent)
    FetchContent_Declare(json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG v3.11.2
    )
    FetchContent_MakeAvailable(json)
endif()

# Source files
set(CORE_SOURCES
    core/cortical_sheet.cpp
    core/tracray_lexicon.cpp
)

set(BRAIN_SOURCES
    brain/seven_region_brain.cpp
    brain/brain_server.cpp
)

set(AGENT_SOURCES
    agents/agent_adapter.cpp
)

# Create static library for core
add_library(aos_core STATIC ${CORE_SOURCES})
target_include_directories(aos_core PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/external
)
target_link_libraries(aos_core PUBLIC 
    nlohmann_json::nlohmann_json
    Threads::Threads
)

# Create static library for brain
add_library(aos_brain_lib STATIC ${BRAIN_SOURCES})
target_include_directories(aos_brain_lib PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}
)
target_link_libraries(aos_brain_lib PUBLIC aos_core)

# Create static library for agents
add_library(aos_agents STATIC ${AGENT_SOURCES})
target_include_directories(aos_agents PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}
)
target_link_libraries(aos_agents PUBLIC aos_brain_lib)

# Main brain daemon executable
add_executable(brain_daemon brain_daemon.cpp)
target_link_libraries(brain_daemon PRIVATE 
    aos_core
    aos_brain_lib
    aos_agents
)

# Brain server executable (HTTP + Unix socket)
add_executable(brain_server brain_server_main.cpp)
target_link_libraries(brain_server PRIVATE 
    aos_core
    aos_brain_lib
    aos_agents
)

# Tests
enable_testing()
add_executable(test_seven_region tests/test_seven_region.cpp)
target_link_libraries(test_seven_region PRIVATE 
    aos_core
    aos_brain_lib
    aos_agents
)
add_test(NAME SevenRegionTest COMMAND test_seven_region)

# Installation
install(TARGETS brain_daemon brain_server
    RUNTIME DESTINATION bin
)

install(DIRECTORY config/ DESTINATION share/aos_brain/config)

# Print summary
message(STATUS "")
message(STATUS "AOS Brain C++ Build Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Install Prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "")
