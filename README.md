libprotobuf for [Unreal Engine 4][]
=====

Link the google's `protocol bufffers` library as the third party in [Unreal Engine 4][].

Prerequisites
-------------

* Python v3 (for install and build scripts)
* depending on you building platform:
  * Windows: [CMake][] and either Visual Studio 2015 or Visual Studio 2017
  * Linux: [clang][] and Unreal Engine Source Code

Usage
-----

1. Clone or add this repository as submodule to your project directory.
2. Go into the just created directory and run `./install.py`. This will build protobuf and copy the compiled version into the ThirdParty directory of your project (`<your project>/ThirdParty/libprotobuf`).
3. Add the libprotobuf as a module into `<your project>.Build.cs`
  * `PrivateDependencyModuleNames.AddRange(new string[] { "CoreUObject", "Engine", "libprotobuf" });`
4. Generate protobuf code files (header & source, ex: Message.pb.h & Message.pb.cc) of your protocol files (.proto) by `protoc` for `cpp` (The protoc executable is located in `<your project>/ThirdParty/libprotobuf/bin`). (Ref: [Google's Protocol Buffers][])
5. Put them into the source directory (`Private` or `Public`) of your project.
6. Regenerate the code file for [Unreal Engine 4][] by `regenerateforue4.py`.
    * `python regenerateforue4.py 'the header file'`
    * ex: `python regenerateforue4.py Message.pb.h`
    * You should get this information: `Success to regenerate the code for UE4`
7. Include and use the header file (ex: Message.pb.h) in your `.cpp` file.
8. That's all.

Reference
-----
1. https://github.com/code4game/libprotobuf
1. https://wiki.unrealengine.com/Standalone_Dedicated_Server
1. https://wiki.unrealengine.com/Linking_Static_Libraries_Using_The_Build_System


[Unreal Engine 4]: https://www.unrealengine.com/
[Google's Protocol Buffers]: https://developers.google.com/protocol-buffers/
[CMake]:http://www.cmake.org
[clang]:https://wiki.unrealengine.com/Compiling_For_Linux
