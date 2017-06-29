import subprocess
import os
import sys
import shutil
import winreg

vs_intermediate     = "_vs_tmp"
protobuf_src_path   = "../../protobuf-source"
libprotobuf_path    = "../../libprotobuf"
prefix_path         = "_prefix"

def create_vs_prj_with_compiler(compiler_version):
    cmd_line = ["cmake", "-G", compiler_version]
    #install prefix
    cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), prefix_path))
    cmd_line.append("-DCMAKE_CONFIGURATION_TYPES=Release")
    cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
    cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
    cmd_line.append(protobuf_src_path+"/cmake")
    subprocess.call(cmd_line)
    
def get_vs2015_devenv():
    try:
        #get visual studio install path
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Microsoft\\VisualStudio\\14.0")
        reg_value, reg_type = winreg.QueryValueEx(reg_key, "InstallDir")
        winreg.CloseKey(reg_key);
        if(reg_type != winreg.REG_SZ):
            print(reg_type)
            return None
        return os.path.join(reg_value, "devenv.com")
    except:
        return None

def get_vs2017_devenv():
    try:
        #get visual studio install path
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Microsoft\\VisualStudio\\SxS\\VS7")
        reg_value, reg_type = winreg.QueryValueEx(reg_key, "15.0")
        winreg.CloseKey(reg_key);
        if(reg_type != winreg.REG_SZ):
            print(reg_type)
            return None
        return os.path.join(reg_value, "Common7", "IDE", "devenv.com")
    except:
        return None

def apply_patch_for_port_h():
    port_h_filepath = os.path.join(prefix_path, "include/google/protobuf/stubs/port.h")
    port_file = open(port_h_filepath, 'r')
    if (port_file is None):
        print("Failed to open the port.h file!!!")
        return
    file_lines = port_file.readlines()
    port_file.close()

    port_file = open(port_h_filepath, 'w')
    if (port_file is None):
        print("Failed to write the port.h file!!!")
        return
    meet_byteswap = False;
    for line in file_lines:
        if (meet_byteswap is False and line[0:21] == "#include <byteswap.h>"):
            port_file.write('''
//BEGIN: by jinchao for UE4(There is a file named ByteSwap.h in Unreal project)
//#include <byteswap.h>  // IWYU pragma: export
#include <bits/byteswap.h>
#define bswap_16(x) __bswap_16 (x)
#define bswap_32(x) __bswap_32 (x)
#define bswap_64(x) __bswap_64 (x)
//END: by jinchao
'''
            )
            meet_byteswap = True
        else:
            port_file.write(line)
    port_file.close()

    
def copy_library():
    target_include = os.path.join(libprotobuf_path, "include");
    if(os.path.exists(target_include)):
        shutil.rmtree(target_include, True)
    shutil.copytree(os.path.join(prefix_path, "include"), target_include)
    
    shutil.copy(os.path.join(prefix_path, "bin/protoc.exe"), os.path.join(libprotobuf_path, "bin/protoc.exe"))
    
    target_lib = os.path.join(libprotobuf_path, "lib/win64");
    if(os.path.exists(target_lib)):
        shutil.rmtree(target_lib, True)
    os.makedirs(target_lib)
    shutil.copy(os.path.join(prefix_path, "lib/libprotobuf.lib"), os.path.join(libprotobuf_path, "lib/win64/libprotobuf.lib"))
    
##################################################

#create intermediate path
if os.path.exists(vs_intermediate):
    shutil.rmtree(vs_intermediate, True)
os.mkdir(vs_intermediate)
os.chdir(vs_intermediate)

#get vs version devenv
vs_compiler_version = "Visual Studio 14 2015 Win64"
devenv_path = get_vs2015_devenv()
if(devenv_path == None):
    vs_compiler_version = "Visual Studio 15 2017 Win64"
    devenv_path = get_vs2017_devenv()
    if(devenv_path == None):
        print("Could neither find VS2015 nor VS2017")
        quit()

#create vs project files
create_vs_prj_with_compiler(vs_compiler_version)

#build vs project 
subprocess.call([devenv_path, "protobuf.sln", "/Build", "Release|x64", "/Project", "INSTALL"])


#copy library files
apply_patch_for_port_h()
copy_library()

