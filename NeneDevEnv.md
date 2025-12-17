# C++開発環境構築
## 前提
- Windows 11 (x64)
- Visual Studio Code

## 手順
1. **Visual Studio Build Tools(VSBT)**
    Visual Studioのエディターはこの世で最も醜いものの一つなので使わず, 中にあるBuild Toolsのみを使います. Visual Studioを入れずにこれだけをインストールできます.
    1. 公式サイト([https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/))の下の方からダウンロード(Tools for Visual Studio → Build Tools for Visual Studio 2022).
    2. C++によるデスクトップ開発にチェックを入れる.
2. **vcpkg**
    パッケージマネージャ. VSBTの中にもvcpkgがありますが, 偽物なので使いません. vcpkgはユーザーディレクトリなどに入れるのが一般的らしいです. (OSの直下にフォルダを作って開発用のツールをまとめる人もいるらしい)
    1. インストールしたい場所で以下を順に実行する.
        ```bash
        # インストール
        git clone https://github.com/microsoft/vcpkg.git

        # bootstrap
        cd vcpkg
        .\bootstrap-vcpkg.bat

        # Visual Studioと統合
        .\vcpkg integrate install
        ```
    2. システム環境変数のPATHに追加
        vcpkg.exeを持っているフォルダのパスをコピーしてPATHに追加します. 最も外側のvcpkgだと思います.
3. **CMake**
    メタビルドシステム. 公式サイト([https://cmake.org/](https://cmake.org/))からインストールします.

4. **母国語を取り戻す**
    現状ではC++のコード内で日本語(UTF-8)を書くとコンパイルに失敗します. そこでWindowsの設定を見直す必要があります.
    1. 設定 → 時刻と言語 → 言語と地域 → 管理用の言語の設定 → システム ロケールの変更 → 「ベータ: ワールドワイド言語サポートでUnicode UTF-8を仕様」にチェックを入れる.
    2. PCを再起動する.
5. **VS Code拡張機能**
    - C/C++
    - CMake Tools
    - GitHub Pull Requests

    あたりがあれば十分だと思います. あとはお好みで.

## サンプルコード
プロジェクトフォルダの直下にCMakeLists.txtを作り, 以下のように書きます. (このファイル名にするとVSCode上でアイコンがMになると思います.)

```cmake
# 00_HelloCpp/CMakeLists.txt

# CMakeの最低バージョンを指定
cmake_minimum_required(VERSION 3.15)

# プロジェクトを定義(HelloCppという名前のCppで書かれたプロジェクト)
# このプロジェクト名はフォルダ名と同じである必要はない
project(HelloCpp LANGUAGES CXX)

# ビルドを実行(main.cppをコンパイルしてhello.exeを作る)
add_executable(hello main.cpp)

```

main.cppを適当に書きます.
```cpp
// 00_HelloCpp/main.cpp

#include <iostream>
#include <vector>
#include <string>

int main() {
  std::cout << "Hello, C++!" << std::endl;
  std::vector<std::string> Zoo = {"dog", "cat", "bird"};
	for (const auto& animal : Zoo){
		std::cout << animal << ' ';
	}
  std::cout << "" << std::endl;
  std::cout << "はろーわーるど！" << std::endl;
  return 0;
}
```

## ビルドと実行

プロジェクトフォルダの直下で以下を順に実行します.
```bash
# buildフォルダを作成・移動
mkdir build && cd build

# キャッシュファイル作成
cmake ..

# Debugフォルダの中に実行ファイルを生成
# 以降, コードを変更したらここからやり直す
cmake --build . --config Debug

# 実行
./Debug/hello.exe
```
## VSCodeからGitHubのリポジトリを操作する方法
### 1. クローン: GitHubのリポジトリを手元の端末にコピーする
1. Gitをインストールしてない場合はインストールする. `git --version`でインストールしているか確認できる. GitHubのアカウントも作ってない場合は作る.
2. VSCodeを開いて, 左下の「Accounts」から「Sign in with GitHub...」を選択.
3. パスワードを入力してサインイン. VSCodeを開く.
4. コマンドパレット(`Ctrl+Shift+P` / `⌘⇧P`)で`Git: Clone`.
5. リポジトリの管理者の場合, 一覧にあるリポジトリからクローンしたいリポジトリを選択. リポジトリの管理者でない場合, クローンしたいリポジトリのURLをペースト.
6. クローン先のフォルダを選択.

### 2. 編集
手元のVSCodeで好きなように編集する. いつでも編集前に戻れるので, 気にせず書きまくってよい(そのためのgit).

### 3. ステージング: どの変更をリポジトリに反映させるか選別する
たいていの編集作業は一つのファイルのみで完結せず, 複数のファイルを編集することになる. コミットコメントでは「何をしたか」を説明する必要があるが, このとき, 各ファイルごとに変更内容を説明する方法もあれば, 複数のファイルの変更をまとめて説明する方法もある. どのファイルの変更に対してコミットを行うかを決める作業をステージングという.

### 4. コミット
ステージングされたファイルに対して, どういう変更を行ったかをコメントして, コミットする.
(ここまでローカルでのGitの操作)

### 5. プッシュ
手元のフォルダ状況をGitHubのリポジトリに反映させる.
