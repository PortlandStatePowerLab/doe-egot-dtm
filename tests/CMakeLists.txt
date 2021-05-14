set(COMPONENT_NAME dtm_testing)

add_executable (${COMPONENT_NAME}
    main.cpp
)

target_link_libraries(${COMPONENT_NAME} 
    gtest 
    gtest_main 
    DCM::https_client
    GSP::https_server
    ${Boost_LIBRARIES} 
    ${PYTHON_LIBRARIES}
    pthread
)

target_include_directories(${COMPONENT_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${GSP_INCLUDE_DIRS}
    ${DCM_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
    ${googletest_INCLUDE_DIRS}
)

add_custom_command(
    TARGET ${COMPONENT_NAME}
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${PROJECT_SOURCE_DIR}/resources/ ${CMAKE_BINARY_DIR}/bin
    ${PROJECT_SOURCE_DIR}/scripts/ ${CMAKE_BINARY_DIR}/bin
)