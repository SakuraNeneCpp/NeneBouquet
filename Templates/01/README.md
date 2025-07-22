# ライブラリのテンプレート
これは成果物がC++のライブラリであるようなプロジェクトフォルダのテンプレートです.

## フォルダ構成
今, `NeneLibrary`というライブラリを作りたいとします. このライブラリは`NeneLib1.hpp`と`NeneLib2.hpp`を提供するものとします.

```
NeneLibrary
    README.md(.txt)
    .gitignore
    .gitmodules
    ref/
        fig/
        01_introduction.md
        ...
    include/
        NeneLibrary/
            NeneLib1.hpp
            NeneLib2.hpp
    src/
        NeneLib1.cpp
        NeneLib2.cpp
    build/
    extern/
    tests/
        CMakeLists.txt
        sandbox.cpp
        testNeneLib1.cpp
        testNeneLib2.cpp
    CMakeLists.txt
    cmake/
        NeneLibraryConfig.cmake.in
```

## .gitignore
```
# Build artefacts
/build*/
*.o
*.obj
*.exe
*.dll
*.so
*.dylib

# IDE
.vscode/
.idea/
*.vcxproj*
```

## (ルート)CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.21)
project(NeneLibrary VERSION 1.0 LANGUAGES CXX)

# オプション例
option(NENE_BUILD_TESTS "Build tests" ON)

# ライブラリ本体
add_library(NeneLibrary
    src/NeneLib1.cpp
    src/NeneLib2.cpp
)
target_include_directories(NeneLibrary PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_compile_features(NeneLibrary PUBLIC cxx_std_20)

# インストール
include(GNUInstallDirs)
install(TARGETS NeneLibrary
        EXPORT NeneLibraryTargets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# パッケージ構成ファイル
install(EXPORT NeneLibraryTargets
        NAMESPACE NeneLibrary::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/NeneLibrary)
configure_file(cmake/NeneLibraryConfig.cmake.in
               ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfig.cmake @ONLY)
install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfig.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/NeneLibrary)

# テスト
if (NENE_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

```