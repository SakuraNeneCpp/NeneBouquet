## なんか`.gitignore`できないファイルがあるんだけど！

一度追跡したファイルを後から`.gitignore`すると失敗する. 履歴から削除しなければならない.
```bash
git rm -r --cached .vscode
```

## コミットしすぎてログが汚いよ！
0) 念のためバックアップ（強く推奨）
```bash
どこからでも戻れるタグ
git tag archive/2025-08-06 HEAD

フルバックアップ（隣に裸クローン）
git clone --mirror . ../repo-backup.git
```
1) ローカルでヒストリーを1コミット化
**Bash**

```bash
newroot=$(git commit-tree HEAD^{tree} -m "fresh start: squash history up to 2025-08-06")
git reset --hard "$newroot"
```
**PowerShell**

```powershell
$newroot = git commit-tree 'HEAD^{tree}' -m 'fresh start: squash history up to 2025-08-06'
git reset --hard $newroot
```
これでローカルのカレントブランチ（例：main）は, いまの内容だけを持つ1つのコミットになる.

2) リモートを上書き（force-with-lease 推奨）
```bash
git push --force-with-lease origin main
```
GitHub等で main が保護ブランチなら, 一時的に「強制プッシュ許可」が必要.

共同開発者は以下で同期可能：

```bash
git fetch
git reset --hard origin/main
```
（再クローンでもOK）

3) お掃除（任意）
```bash
git gc --prune=now
```

## 会社で`git clone`ができない！
windowsでは, ブラウザはプロキシを通すのにGitは直接接続しようとしてタイムアウトになったりする. `git config`にプロキシ設定を明記する必要がある.

今, プロキシサーバのアドレスが`http://proxy.example:8080`であるならば,
```powershell
git config --global http.proxy http://proxy.example:8080
git config --global https.proxy http://proxy.example:8080
```

## 自分のリポジトリなのにプッシュできない！
古いGitHubアカウントが残っている可能性がある. 「コントロールパネル」→「ユーザーアカウント」→「資格情報マネージャー」→「Windowsの資格情報」から古いGitHubアカウントを削除し, VSCodeを再起動.


## 編集者の名義をPCのユーザー名から変更したい！
Gitではコミットの “Author/Committer” に user.name と user.email が使われる. 未設定のときはOSのユーザー名が自動で入る. これはGitHub上でコードの編集者として表示される. 変更するときは以下を実行.

``` bash
# すべてのリポジトリで共通にしたい場合
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"

# 今のリポジトリだけ変えたい場合
git config --local  user.name  "Your Name"
git config --local  user.email "you@example.com"