# ライブラリのテンプレート
これは成果物がC++のライブラリであるようなプロジェクトフォルダのテンプレートです.

## フォルダ構成
今, `NeneLibrary`というライブラリを作りたいとします. このライブラリは`NeneLib1.hpp`と`NeneLib2.hpp`を提供するものとします.

```
NeneLibrary/
    README.md(.txt)
    LICENSE.txt
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
        NeneIcecream/
        googletest/
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
cmake_minimum_required(VERSION 3.21) # 最低CMakeバージョン宣言
project(NeneLibrary VERSION 1.0 LANGUAGES CXX) # プロジェクト名, バージョン, 言語

# ビルドオプション
option(NENE_BUILD_SANDBOX "Build sandbox executable" ON)
option(NENE_BUILD_TESTS "Build tests" ON)

# ライブラリ本体
add_library(NeneLibrary # NeneLibraryというビルドターゲットを生成
    src/NeneLib1.cpp    # ソース列挙
    src/NeneLib2.cpp
)
target_include_directories(NeneLibrary PUBLIC # インクルードディレクトリ公開
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_compile_features(NeneLibrary PUBLIC cxx_std_20) # 利用にはC++20以上を要求

# インストール
include(GNUInstallDirs)
install(TARGETS NeneLibrary
        EXPORT NeneLibraryTargets
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# パッケージ構成ファイル
include(CMakePackageConfigHelpers)
configure_file(cmake/NeneLibraryConfig.cmake.in
               ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfig.cmake @ONLY)
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
)
install(FILES
        ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/NeneLibraryConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/NeneLibrary)

# テスト
if (NENE_BUILD_SANDBOX OR NENE_BUILD_TESTS)
    add_subdirectory(tests)
endif()

```

## NeneLibraryConfig.cmake.in
```cmake
@PACKAGE_INIT@
include(CMakeFindDependencyMacro)

include("${CMAKE_CURRENT_LIST_DIR}/NeneLibraryTargets.cmake")

# set(NeneLibrary_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include")
set(NeneLibrary_VERSION "@PROJECT_VERSION@")

check_required_components(NeneLibrary)
```

## tests/CMakeLists.txt
```cmake
# Sandbox と UnitTest を独立制御
if (NOT DEFINED NENE_BUILD_SANDBOX)
  set(NENE_BUILD_SANDBOX ON CACHE BOOL "Build sandbox executable")
endif()
if (NOT DEFINED NENE_BUILD_UNIT_TESTS)
  set(NENE_BUILD_UNIT_TESTS ${NENE_BUILD_TESTS} CACHE BOOL "Build GoogleTest-based unit tests")
endif()
if (NOT DEFINED NENE_USE_SUBMODULE_GTEST)
  set(NENE_USE_SUBMODULE_GTEST ON CACHE BOOL "Use embedded googletest submodule")
endif()

# extern ディレクトリ（プロジェクト直下想定）
set(EXTERN_DIR "${PROJECT_SOURCE_DIR}/extern")

# --------------------------------------------------------------------------
# 1 Sandbox
# --------------------------------------------------------------------------
if (NENE_BUILD_SANDBOX)
    add_executable(nene_sandbox sandbox.cpp)
    target_link_libraries(nene_sandbox PRIVATE NeneLibrary)

    # --- NeneIcecream（ヘッダオンリー or 付属CMakeあり のどちらにも対応）---
    if (EXISTS "${EXTERN_DIR}/NeneIcecream/CMakeLists.txt")
        # もし NeneIcecream 自体が CMake 対応なら
        add_subdirectory("${EXTERN_DIR}/NeneIcecream" "${CMAKE_BINARY_DIR}/_icecream")
        # target が NeneIcecream という名前とは限らないので要確認
        # target_link_libraries(nene_sandbox PRIVATE NeneIcecream)
    elseif (EXISTS "${EXTERN_DIR}/NeneIcecream/include")
        # ヘッダオンリー体制
        target_include_directories(nene_sandbox PRIVATE "${EXTERN_DIR}/NeneIcecream/include")
        target_compile_definitions(nene_sandbox PRIVATE NENE_HAVE_ICECREAM=1)
    endif()
endif()

# --------------------------------------------------------------------------
# 2 Unit Tests (GoogleTest)
# --------------------------------------------------------------------------
if (NENE_BUILD_UNIT_TESTS)
    enable_testing()  # ルートでも呼んでいるなら二重でも安全

    if (NENE_USE_SUBMODULE_GTEST)
        add_subdirectory("${EXTERN_DIR}/googletest" EXCLUDE_FROM_ALL)
        if (TARGET GTest::gtest_main)
            set(GTEST_LIBS GTest::gtest_main GTest::gtest)
        else()
            set(GTEST_LIBS gtest_main gtest)
        endif()
    else()
        find_package(GTest CONFIG REQUIRED)
        set(GTEST_LIBS GTest::gtest_main GTest::gtest)
    endif()

    # ---- テスト1 ----------------------------------------------------------
    add_executable(testNeneLib1 testNeneLib1.cpp)
    target_link_libraries(testNeneLib1 PRIVATE NeneLibrary ${GTEST_LIBS})
    add_test(NAME NeneLib1Unit COMMAND testNeneLib1)

    # ---- テスト2 ----------------------------------------------------------
    add_executable(testNeneLib2 testNeneLib2.cpp)
    target_link_libraries(testNeneLib2 PRIVATE NeneLibrary ${GTEST_LIBS})
    add_test(NAME NeneLib2Unit COMMAND testNeneLib2)

    # （任意）自動テスト検出を使いたい場合
    include(GoogleTest OPTIONAL RESULT_VARIABLE _gtest_found)
    if (_gtest_found)
        gtest_discover_tests(testNeneLib1)
        gtest_discover_tests(testNeneLib2)
    endif()
endif()
```