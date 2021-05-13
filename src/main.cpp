#include <boost/python.hpp>
#include <iostream>
#include <stdlib.h>
#include <thread>         // std::thread
#include <string>


using namespace boost::python;

std::string g_program_path;

void GetParentPath(char** arg)
{
    g_program_path = arg[0];
    std::size_t found = g_program_path.find_last_of("/\\");
    g_program_path = g_program_path.substr(0,found);
};


void SpawnDTM(const std::string &file_path, int argc, wchar_t **wargv)
{
try
    {
        Py_Initialize();
        PySys_SetArgv(argc, wargv);
        object _mainModule = import("__main__");
        object _mainNamespace = _mainModule.attr("__dict__");

        //Testing executing a python script file
        //exec_file("script.py", _mainNamespace, _mainNamespace);
        //Run a simple file
        FILE* PScriptFile = fopen(file_path.c_str(), "r");
        if(PScriptFile){
            PyRun_SimpleFile(PScriptFile, file_path.c_str());
            fclose(PScriptFile);
        }
    }
    catch (error_already_set)
    {
        PyErr_Print();
    }
};

int main(int argc, char **argv)
{

    wchar_t** wargv = new wchar_t*[argc];
    for(int i = 0; i < argc; i++)
    {
        wargv[i] = Py_DecodeLocale(argv[i], nullptr);
        if(wargv[i] == nullptr)
        {
            return EXIT_FAILURE;
        }
    }

    GetParentPath(argv);
    std::string script_path = g_program_path + "/dtm_server.py";
    std::thread dtm (SpawnDTM, script_path, argc, wargv);
    
    // synchronize threads:
    dtm.join(); 
}
