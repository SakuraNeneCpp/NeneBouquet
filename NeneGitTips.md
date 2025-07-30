
一度追跡したファイルを後から`.gitignore`すると失敗する. 履歴から削除しなければならない.
```bash
git rm -r --cached .vscode
```