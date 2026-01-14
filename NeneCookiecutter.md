# NeneCookiecutter
windowsの場合.
1. Pythonを入れる  
webサイトのインストーラから入れるのが無難かも.

2. pipxを入れてパスを通す.
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```
ここでいったんターミナルを閉じる.

3. Cookiecutterを入れる.
```bash
pipx install cookiecutter
```

4. テンプレートを再現する.
プロジェクトフォルダを置きたい場所で以下を実行. (URLは適宜変更する)
```bash
cookiecutter https://github.com/SakuraNeneCpp/NeneCppTestArea
```