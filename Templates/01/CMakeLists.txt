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