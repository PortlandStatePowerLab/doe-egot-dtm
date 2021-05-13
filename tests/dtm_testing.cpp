#include <iostream>
#include <string>
#include <sstream>
#include <gtest/gtest.h>
#include <https/https_client.hpp>
#include <https/https_server.hpp>

extern std::string g_program_path;

class DTMTesting : public ::testing::Test 
{
protected:
    void SetUp() override 
    {        
        host = "0.0.0.0";
        port = "443";
        client = new HttpsClient(g_program_path, host, port);
        server = new HttpsServer(host, 443, g_program_path);
        dtm = new HttpsServer(host, 4430, g_program_path);
    }

    void TearDown() override
    {
        delete client;
        delete server;
    }

    std::string host;
    std::string port;
    HttpsClient *client;
    HttpsServer *server;
    HttpsServer *dtm;
};

TEST_F(DTMTesting, DeviceCapability) 
{   
    client->Post("/na", "testing testing testing");
    auto resp = client->Get("/dcap");
    std::string body = boost::beast::buffers_to_string(resp.body().data());
    std::cout << resp << std::endl;
    client->Post("/na", body);
    std::cout << resp << std::endl;    
}
