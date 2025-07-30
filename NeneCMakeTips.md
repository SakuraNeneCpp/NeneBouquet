ビルド時になんか気になる文章が出てくる
```
'pwsh.exe' is not recognized as an internal or external command, operable program or batch file.
```

多くの場合で無害だけど, PowerShell7をインストールしておくと消せる.

1. インストール  
```bash
winget install --id Microsoft.PowerShell -e
```

2. PATHを通す  
`C:\Program Files\PowerShell\7\` をシステム環境変数のPATHに追加

3. CMake 側でフォールバックを明示
```cmake
# CMakeLists.txt のどこかで
find_program(POWERSHELL_EXE NAMES pwsh.exe powershell.exe)
if(NOT POWERSHELL_EXE)
  message(STATUS "PowerShell not found; skipping optional steps")
endif()

# 使うときは ${POWERSHELL_EXE} を呼ぶ
add_custom_command(
  OUTPUT something
  COMMAND "${POWERSHELL_EXE}" -NoProfile -ExecutionPolicy Bypass -File ${CMAKE_SOURCE_DIR}/scripts/do.ps1
  DEPENDS scripts/do.ps1
)

```