set(COMPONENT_NAME dtm)
add_executable(${COMPONENT_NAME} main.cpp)

# Set up the libraries and header search paths for this target
target_link_libraries(${COMPONENT_NAME} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} pthread)
target_include_directories(
    ${COMPONENT_NAME} PUBLIC 
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
)

add_custom_command(
    TARGET ${COMPONENT_NAME}
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${PROJECT_SOURCE_DIR}/resources/ ${CMAKE_BINARY_DIR}/bin
    ${PROJECT_SOURCE_DIR}/scripts/ ${CMAKE_BINARY_DIR}/bin
)