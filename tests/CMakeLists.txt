set(COMPONENT_NAME dtm_testing)

add_executable (${COMPONENT_NAME}
    main.cpp
    dtm_testing.cpp
)

target_link_libraries(${COMPONENT_NAME} 
    gtest 
    gtest_main 
    Boost::boost
    DCM::https_client
    GSP::https_server
    pthread
)

target_include_directories(${COMPONENT_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${GSP_INCLUDE_DIRS}
    ${DCM_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    ${googletest_INCLUDE_DIRS}
)