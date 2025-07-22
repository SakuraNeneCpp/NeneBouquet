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