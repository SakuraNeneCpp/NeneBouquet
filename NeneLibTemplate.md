# ライブラリのテンプレート
これは成果物がC++のライブラリであるようなプロジェクトのテンプレートです.

## フォルダ構成
今, `NeneLibrary`というライブラリを作りたいとします. このライブラリは`NeneLib1.hpp`と`NeneLib2.hpp`を提供するものとします.

```
NeneLibrary/
    README.md(.txt)
    LICENSE.txt
    .gitignore
    .gitmodules
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
        NenePancake/
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
option(BUILD_SANDBOX "Build sandbox executable" ON)
option(BUILD_TESTS "Build tests" ON)

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
if (BUILD_SANDBOX OR BUILD_TESTS)
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
if (NOT DEFINED BUILD_SANDBOX)
  set(BUILD_SANDBOX ON CACHE BOOL "Build sandbox executable")
endif()
if (NOT DEFINED BUILD_UNIT_TESTS)
  set(BUILD_UNIT_TESTS ${BUILD_TESTS} CACHE BOOL "Build unit tests executable")
endif()

# extern ディレクトリ（プロジェクト直下想定）
set(EXTERN_DIR "${PROJECT_SOURCE_DIR}/extern")

# Sandbox
if (BUILD_SANDBOX)
    add_subdirectory("${EXTERN_DIR}/NeneIcecream" "${CMAKE_CURRENT_BINARY_DIR}/_icecream")
    add_executable(sandbox sandbox.cpp)
    target_link_libraries(sandbox PRIVATE NeneLibrary NeneIcecream::NeneIcecream)
endif()

# Unit Tests
if (BUILD_UNIT_TESTS)
    add_subdirectory("${EXTERN_DIR}/NenePancake" "${CMAKE_CURRENT_BINARY_DIR}/_pancake")
    # テスト1
    add_executable(testNeneLib1 testNeneLib1.cpp)
    target_link_libraries(testNeneLib1 PRIVATE NeneLibrary NenePancake::NenePancake)
    # テスト2
    add_executable(testNeneLib2 testNeneLib2.cpp)
    target_link_libraries(testNeneLib2 PRIVATE NeneLibrary NenePancake::NenePancake)
endif()
```

## NeneLib1, NeneLib2
(以下は例)
```cpp
// NeneLib1.hpp
#pragma once
#include <string>
namespace nene {
// ライブラリが定数を提供する例
inline constexpr int kMagicNumber = 42;
// ライブラリが関数を提供する例
// 与えられた文字列の前に "Nene" を付けて返す
[[nodiscard]] std::string decorate(const std::string& msg);
} // namespace nene
```
```cpp
// NeneLib1.cpp
#include "NeneLibrary/NeneLib1.hpp"
namespace nene {
std::string decorate(const std::string& msg) {
    return "Nene: " + msg;
}
} // namespace nene
```
```cpp
// NeneLib2.hpp
#pragma once
#include <string>
namespace nene {
// ライブラリがクラスを提供する例
class Counter {
public:
    explicit Counter(int start = 0) noexcept : value_{start} {}
    void increment(int delta = 1) noexcept { value_ += delta; }
    void reset(int v = 0) noexcept { value_ = v; }
    [[nodiscard]] int value() const noexcept { return value_; }
    // 例として、現在値を文字列化して返すメソッド
    [[nodiscard]] std::string to_string() const {
        return "Counter(" + std::to_string(value_) + ")";
    }
private:
    int value_{};
};
} // namespace nene
```
```cpp
// NeneLib2.cpp
#include "NeneLibrary/NeneLib2.hpp"
// メンバはすべてインライン実装で完結しているため.cppに書くことはない. 特にtemplate<>を使うと, 実装を分離できないため, こういうことがよく起きる.
namespace nene {
// 例として to_string() をこちらに移したい場合:
// std::string Counter::to_string() const { return "Counter(" + std::to_string(value_) + ")"; }
}
```

## 開発手順
以降, すべてのコマンドをルート直下 `NeneLibrary/` で実行するものとします.
### 1. フォルダ構築
```
NeneLibrary/
    README.md(.txt)
    LICENSE.txt
    .gitignore
    .gitmodules
    include/
        NeneLibrary/
            NeneLib1.hpp
            NeneLib2.hpp
    src/
        NeneLib1.cpp
        NeneLib2.cpp
    tests/
        CMakeLists.txt
        sandbox.cpp
        testNeneLib1.cpp
        testNeneLib2.cpp
    CMakeLists.txt
    cmake/
        NeneLibraryConfig.cmake.in
```
ここまでフォルダを構成します. 他は以降の操作で自動的に生成されます. 以下のコマンドを使用することで一括で作成できます:
```bash
# 後で作る
```
### 2. git config
```bash
git init
git config --local user.name "SakuraNene"
git config --local user.email "skrnn0505@gmail.com"
```
### 3. git submodules
```bash
git submodule add https://github.com/SakuraNeneCpp/NeneIcecream.git extern/NeneIcecream
git submodule add https://github.com/SakuraNeneCpp/NenePancake.git extern/NenePancake
git submodule update --init --recursive
```
### 4. コーディング
(頑張って書く)

### 5. ビルド
#### A. サンドボックス / テスト
```bash
# 下のコマンドのON/OFFを切り替える
cmake -S . -B build -DBUILD_SANDBOX=ON -DBUILD_TESTS=OFF
cmake --build build --config Debug -j
./build/tests/Debug/sandbox.exe
# 実行ファイルの場所は環境によって異なる
```
#### B. リリースビルド
```bash
cmake -S . -B build -DBUILD_SANDBOX=OFF -DBUILD_TESTS=OFF
cmake --build build --config Release -j
```


## 命名と変換
最低でも, 以下を各自で命名する必要があります.

| 対象 | NeneLibraryの場合 ||
| --- | --- | --- |
| プロジェクト名(=ライブラリ名) | NeneLibrary ||
| ヘッダファイル名(=実装ファイル名) | NeneLib1, NeneLib2 ||
| テストファイル名(=ビルド時の実行ファイル名) | testNeneLib1, testNeneLib2 ||

コピーした後で一斉に置換してしまうのが一番楽です.
