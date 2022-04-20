# Python Project Template

最近、Python の新しいプロジェクトを立ち上げる度に毎回同じような設定をコピペしていたので、テンプレートを用意しとこうと思った次第です。

- [Python Project Template](#python-project-template)
  - [採用技術](#採用技術)
  - [前提となるツール](#前提となるツール)
  - [Python バージョン管理](#python-バージョン管理)
    - [pyenv](#pyenv)
  - [パッケージマネージャー](#パッケージマネージャー)
    - [poetry](#poetry)
  - [リンター (linter)](#リンター-linter)
    - [flake8](#flake8)
      - [flake8 プラグイン](#flake8-プラグイン)
    - [mypy](#mypy)
  - [フォーマッター (formatter)](#フォーマッター-formatter)
    - [black](#black)
    - [isort](#isort)
  - [テスティングフレームワーク](#テスティングフレームワーク)
    - [pytest](#pytest)
  - [ドキュメント生成](#ドキュメント生成)
    - [sphinx](#sphinx)
  - [タスクランナー](#タスクランナー)
    - [taskipy](#taskipy)
  - [Git Hooks](#git-hooks)
    - [pre-commit](#pre-commit)
  - [CI/CD](#cicd)
    - [GitHub Actions](#github-actions)
  - [VSCode](#vscode)
    - [settings.json](#settingsjson)
    - [extensions.json](#extensionsjson)

## 採用技術

- python 3.10
- poetry (パッケージ管理)
- flake8, mypy (リンター)
- black, isort (フォーマッター)
- pytest (テスティングフレームワーク)
- sphinx (ドキュメント生成)
- taskipy (タスクランナー)
- pre-commit (git フック)
- github actions (CI/CD)
- vscode (エディタ)

パッケージ管理には `pipenv` ではなく `poetry` を採用し、  
ドキュメント生成には `sphinx` を採用し、  
エディタには `vscode` を採用し、  
CI/CD は `github actions` でやっちゃってる感じです。

当リポジトリを参考にしてくださる方がいる場合は適時不要な技術に関連する設定ファイルは消しちゃって下さい。

## 前提となるツール

- git
- pyenv
- poetry

この3つはお使いのマシン上で使える状態になっている前提です。  
`pyenv` や `poetry` のインストール方法やコマンドの解説も省略しております。

## Python バージョン管理

### pyenv

プロジェクトが変われば使用する `python` のバージョンも変わるのが普通なので、同じマシン上でも複数の `python` バージョンを切り替えれるようにしておく必要があり、`pyenv` を採用しています。

## パッケージマネージャー

### poetry

`python` のパッケージマネージャーだと `poetry` と `pipenv` が有名ですが、比較記事がたくさんあるので詳しくはググってください。

ただし、 **インストールについては、公式ドキュメントに書いてある「With the official installer」の方法で行うことをおすすめします** 。

<https://python-poetry.org/docs/master/#installing-with-the-official-installer>

というのも、記事によっては上記公式ドキュメントの「With the official installer」の方ではなく「With pip」のインストール方法が紹介されているのですが、`pip install poetry` でのインストールとなると **pyenv でインストールした python バージョン毎に管理されている `site-packages` ディレクトリ** にインストールされます。

そのため、pyenv でグローバルの python バージョンを切り替えたら poetry コマンドも使えなくなります。

加えて、公式ドキュメントにも

> Be aware that it will also install Poetry’s dependencies which might cause conflicts with other packages.

と、他パッケージとの競合に気をつけろよとの警告文があるので、基本的には pip でのインストールはしないほうがいいでしょう。

## リンター (linter)

### flake8

python のスタイルガイドである `PEP8` にコードが準拠されているかを検査するリンターとして `pycodestyle` というものがあるのですが、`flake8` は `pycodestyle` を内蔵しており、それに加えて論理エラーまでチェックしてくれるという代物です。

`pycodestyle` より厳しいリンターと認識しておけばいいと思います。

```shell
poetry add -D flake8
```

で開発用パッケージとしてプロジェクトに追加します。

#### flake8 プラグイン

`flake8` にはプラグインがたくさんあり、入れれば入れるほど厳しい設定になっていきます。

自分で細かくオプションを設定していくことも出来ますが、個人的にはリンターやフォーマッターの設定って凝りすぎると設定ファイルを書く作業にかかる時間がアホみたいに長くなったり、プロジェクト毎のルールの乖離が大きくなってしまってデメリットが大きくなっていくと思っていて(特に `js, ts` のプロジェクトは設定ファイルまみれになるのが苦手...)、極力リンターの設定強化は設定ファイルで行うのではなくプラグインの追加だけで済ませたいという考えです。

```shell
poetry add -D flake8-isort flake8-bugbear flake8-builtins flake8-eradicate flake8-unused-arguments flake8-pytest-style pep8-naming
```

自分は大体上記のプラグインを追加することが多いです。

- flake8-isort
  - import 順が isort (後述) に準拠しているかチェック
- flake8-bugbear
  - バグが出やすい箇所に警告を出してくれる
- flake8-builtins
  - 変数名/関数名が組み込みオブジェクトと被っていないかチェック
- flake8-eradicate
  - コメントアウトされているコードがないかチェック
- flake8-unused-arguments
  - 未使用引数がないかチェック
  - AWS Lambda の場合 handler の context を使わないケースが多いのでこのプラグインは不向きかもです
- flake8-pytest-style
  - pytest (後述) 用のスタイルチェク
- pep8-naming
  - 変数名/関数名が PEP8 に準拠しているかチェック

これ以外にもプラグインはたくさんあるので探してみるとお好みのものが見つかるかもしれません。

以下コマンドで `src` ディレクトリ及び `tests` ディレクトリに対して実行出来ます。  
このとき、`flake8` コマンドしか実行していませんが、プラグインを追加している場合はそのプラグインの検査も含まれています。

```shell
poetry run flake8 src tests
```

※ 以下 `poetry run` から始まる全てのコマンドの共通事項として、`poetry shell` 後であれば `poetry run` は省略可能 (`flake8 src test` だけでOK) です。

### mypy

言わずと知れた、`python` で静的型検査をしてくれるツールです。  
バグの低減はもちろん、`vscode` 上での補完もゴリゴリに効くようになってコーディングが捗ります。

```shell
poetry add -D mypy
```

で開発用パッケージとしてプロジェクトに追加します。

加えて、以下のような設定を `pyproject.toml` に記述しています。  
テンプレートリポジトリの方ではコメントを書いてませんが、ここでは解説のため各行にコメントを付け加えています。

```toml:pyproject.toml
[tool.mypy]
# エラー時のメッセージを詳細表示
show_error_context = true
# エラー発生箇所の行数/列数を表示
show_column_numbers = true
# import 先のチェックを行わない (デフォルトだとサードパーティーライブラリまでチェックする)
ignore_missing_imports = true
# 関数定義の引数/戻り値に型アノテーション必須
disallow_untyped_defs = true
# デフォルト引数に None を取る場合型アノテーションに Optional 必須
no_implicit_optional = true
# 戻り値が Any 型ではない関数の戻り値の型アノテーションが Any のとき警告
warn_return_any = true
# mypy エラーに該当しない箇所に `# type: ignore` コメントが付与されていたら警告
# ※ `# type: ignore` が付与されている箇所は mypy のエラーを無視出来る
warn_unused_ignores = true
# 冗長なキャストに警告
warn_redundant_casts = true
```

以下コマンドで `src` ディレクトリ及び `tests` ディレクトリに対して実行出来ます。

```shell
poetry run mypy src tests
```

## フォーマッター (formatter)

### black

総合的な `python` フォーマッターで、`eslint` など他言語のフォーマッターと比べて自分で設定する箇所が少ないところが気に入っています。

```shell
poetry add -D black
```

で開発用パッケージとしてプロジェクトに追加します。

デフォルトだと1行の最大文字数が 88 になっているのですが、`PEP8` に合わせて79文字にするため、`pyproject.toml` に以下の設定をしています。

```toml:pyproject.toml
[tool.black]
line-length = 79
```

この辺は好みなので気にならない人は設定しなくてもいいと思います。

以下コマンドで `src` ディレクトリ及び `tests` ディレクトリに対して実行出来ます。

```shell
poetry run black src tests
```

また、`--check` オプションを付与することで、フォーマットを実行せずに「フォーマットが必要な箇所があるか」を検査出来ます。
`CI` 等で `lint` のステップに組み込むと良いです。

```shell
poetry run black --check src tests
```

### isort

`import` の順番を

1. 組み込みライブラリ
2. サードパーティーライブラリ
3. 自作ライブラリ

かつ、1~3 の中でアルファベット順に並び替えてくれます。

```shell
poetry add -D isort
```

で開発用パッケージとしてプロジェクトに追加します。

`black` と併用する都合 `pyproject.toml` に以下の設定をしています。

```toml:pyproject.toml
[tool.isort]
profile = "black"
line_length = 79
```

以下コマンドで `src` ディレクトリ及び `tests` ディレクトリに対して実行出来ます。

```shell
poetry run isort src tests
```

## テスティングフレームワーク

### pytest

たぶんデファクトスタンダードでしょう。  
テストコードを書かない場合は不要です。

```shell
poetry add -D pytest pytest-mock pytest-cov
```

で開発用パッケージとしてプロジェクトに追加します。

`pytest-mock` はモック作成用、`pytest-cov` はカバレッジ出力のために使用します。

カバレッジ出力を `html` で行うと以下のような形になります。

```shell
poetry run pytest -s -vv --cov=. --cov-report=html
```

![pytest-cov-1](https://storage.googleapis.com/zenn-user-upload/c34e0735a18a-20220418.png)
![pytest-cov-2](https://storage.googleapis.com/zenn-user-upload/35ff38778061-20220418.png)

テストコードの書き方についてはここでは触れませんが、リポジトリに簡単なサンプルだけ含まれてます。

## ドキュメント生成

### sphinx

ドキュメントの生成には `sphinx` を採用してます。  
`python` のライブラリのドキュメントでよく見かける [こんな見た目のやつ](https://sphinx-rtd-theme.readthedocs.io/en/stable/) です

```shell
poetry add -D Sphinx sphinx-rtd-theme sphinx-pyproject
```

で開発用パッケージとしてプロジェクトに追加します。

`sphinx-rtd-theme` はテーマを [これ](https://sphinx-rtd-theme.readthedocs.io/en/stable/) にするために、`sphinx-pyproject` は `sphinx` の設定を `pyproject.toml` で一元管理するためにインストールしています。

`pyproject.toml` に以下の記述を追記します。  
各パラメータに設定している値は適時修正してください。

```toml:pyproject.toml
[project]
name = "python-template"
version = "0.1.0"
description = "Python Project の Template"
readme = "README.md"

[[project.authors]]
name = "jDBTISK"

[tool.sphinx-pyproject]
project = "python-template"
copyright = "2022, jDBTISK"
language = "en"
package_root = "python-template"
html_theme = "sphinx_rtd_theme"
todo_include_todos = true
templates_path = ["_templates"]
html_static_path = ["_static"]
extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.viewcode",
  "sphinx.ext.todo",
  "sphinx.ext.napoleon",
]
```

加えて、`docs/source/conf.py` を作成します。  
`sphinx-pyproject` を使用していない場合、このファイルに上記の `pyproject.toml` に追記したような内容を書いていかなければいけないんですが、ここでは以下のコードをコピペするだけで OK です。

```python:docs/source/conf.py
import os
import sys

from sphinx_pyproject import SphinxConfig

sys.path.append(
    os.path.abspath(f"{os.path.dirname(os.path.abspath(__file__))}/../../")
)

config = SphinxConfig("../../pyproject.toml", globalns=globals())
```

この設定でテンプレートリポジトリに含まれているソースコードを対象にドキュメントを生成すると以下のようになります。

```shell
poetry run sphinx-apidoc -F -o docs/source src
poetry run sphinx-build docs/source docs/build
```

![sphinx-1](https://storage.googleapis.com/zenn-user-upload/47691d38da65-20220418.png)
![sphinx-2](https://storage.googleapis.com/zenn-user-upload/b67d37f8502e-20220418.png)

## タスクランナー

### taskipy

タスクランナーというのは簡単に言うと `node` で言う `npm run ~~~` みたいにコマンドのエイリアスを設定ファイルに書いておけるやつです。

`poetry` にはデフォルトでタスクランナーが搭載されているわけではないですが、サードパーティーの `taskipy` というライブラリをインストールすることでタスクランナーを使用出来ます。

```shell
poetry add -D taskipy
```

で開発用パッケージとしてプロジェクトに追加します。

タスクランナーとして使うためには `pyproject.toml` に以下のような記述をします。

```toml:pyproject.toml
[tool.taskipy.tasks]
test = "pytest -s -vv --cov=. --cov-report=html"
fmt = "task fmt-black && task fmt-isort"
fmt-black = "black src tests"
fmt-isort = "isort src tests"
lint = "task lint-black && task lint-flake8 && task lint-mypy"
lint-flake8 = "flake8 src tests"
lint-mypy = "mypy src tests"
lint-black = "black --check src tests"
docs = "sphinx-apidoc -F -o docs/source src && sphinx-build docs/source docs/build"
```

実行コマンドは `poetry run task タスク名` です。  
これでフォーマッターやリンター、ドキュメント生成等のコマンドをいちいち覚える必要がなくなるので楽です。

```shell
# テスト実行
poetry run task test
# フォーマッター実行
poetry run task fmt
# リンター実行
poetry run task lint
# ドキュメント出力
poetry run task docs
```

`poetry shell` 中であれば `poetry run` を省略出来るので `task test` だけでテスト実行になります。

## Git Hooks

### pre-commit

`.pre-commit-config.yaml` という設定ファイルを使って `pre-commit` の設定が出来ます。

`pre-commit` というのは `git commit` 実行時にコミット前に走るスクリプトになります。

```shell
poetry add -D pre-commit
```

で開発用パッケージとしてプロジェクトに追加します。

`.pre-commit-config.yaml` ファイルをプロジェクトのルートに作成します。  
テンプレートリポジトリの方ではコメントを書いてませんが、ここでは解説のためコメントを付け加えています。

```yml:.pre-commit-config.yaml
repos:
  # hooks script のソースリポジトリ
  - repo: https://github.com/pre-commit/pre-commit-hooks
    # リポジトリのブランチ or タグ
    rev: v4.2.0
    # 使用したい hook script の指定
    hooks:
      # markdown 以外の行末スペース削除
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]
      # ファイル最終行を改行コードにする
      - id: end-of-file-fixer
      # 改行コードを LF に統一
      - id: mixed-line-ending
        args: [--fix=lf]
      # 巨大なファイルの commit を禁止
      - id: check-added-large-files
      # toml 構文チェック
      - id: check-toml
      # yaml 構文チェック
      - id: check-yaml
      # aws の認証情報が含まれていないかチェック
      - id: detect-aws-credentials
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      # black によるフォーマット実行
      - id: black
        language_version: python3
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.942
    hooks:
    # mypy による型チェック実行
    - id: mypy
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      # isort によるフォーマット実行
      - id: isort
  - repo: https://gitlab.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      # flake8 によるコードチェック実行
      - id: flake8
        # 使用する flake8 プラグイン
        additional_dependencies:
          - flake8-isort
          - flake8-bugbear
          - flake8-builtins
          - flake8-eradicate
          - flake8-pytest-style
          - flake8-unused-arguments
          - pep8-naming
```

このファイルを書いたら、以下コマンドで `git hook` スクリプトをセットアップします。

```shell
poetry run pre-commit install
```

以降、このリポジトリで `git commit` しようとすると `.pre-commit-config.yaml` に書いた設定に従った各種チェックが入り、違反しているものがあればコミット自体されません。

## CI/CD

### GitHub Actions

これに関しては好みの差以前に利用する `git` のホスティングサービスによって使えるものが変わったりもすると思いますが、とりあえず自分が `github` で `python` リポジトリ作る場合によく書く `workflow` になります。

```yml:.github/workflows/lint.yml
name: python lint

on:
  # main ブランチ向けのプルリク作成時、及び
  # main ブランチ向けプルリクのソースブランチへの push 時に workflow 実行
  pull_request:
    branches:
      - main
    # python ファイル or 使用するライブラリ (poetry.lock) or このファイル
    # に変更があったときだけ workflow 実行
    paths:
      - "src/**.py"
      - "tests/**.py"
      - "poetry.lock"
      - ".github/workflows/lint.yml"

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      # ここで指定するバージョンを増やせば複数の python バージョンで各 step を実行出来ます
      # ライブラリを作っていて対応している python バージョン全てで test を行いたいときに便利です
      matrix:
        python-version: ["3.10"]

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Poetry
        run: |
          curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
          echo "$HOME/.poetry/bin" >> $GITHUB_PATH

      # .venv ディレクトリをキャッシュ
      - uses: actions/cache@v2
        id: venv_cache
        with:
          path: .venv
          key: venv-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}

      # poetry.lock ファイルに変更がなければキャッシュされている .venv を使用
      - name: Install Dependencies
        if: steps.venv_cache.outputs.cache-hit != 'true'
        run: poetry install

      - name: Python Lint
        run: poetry run task lint

      - name: Python Test
        run: poetry run task test
```

加えてデプロイ用の workflow も入ってくる感じになると思いますが、デプロイ先によって全然違うものになってくるのでテンプレートには含めていません。

## VSCode

### settings.json

`vscode` を使用する場合、プロジェクトのルートに `.vscode/settings.json` があるとその設定がプロジェクト内のみ有効になります。

```json:.vscode/settings.json
{
  "[python]": {
    // タブサイズは 4
    "editor.tabSize": 4,
    // ファイル保存時にフォーマット
    "editor.formatOnSave": true
  },
  // tests ディレクトリから src ディレクトリのモジュールをインポートするときの vscode 上でモジュールが見つからないエラー防止
  "python.analysis.extraPaths": ["./src"],
  // .venv 内の python を使用
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  // フォーマッターは black を使用
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
  "python.sortImports.path": "${workspaceFolder}/.venv/bin/isort",
  // リンターに flake8 と mypy を使用
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Path": "${workspaceFolder}/.venv/bin/flake8",
  "python.linting.mypyEnabled": true,
  "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
  // docstring は nympy スタイル (ここは完全好みです)
  "autoDocstring.docstringFormat": "numpy"
}
```

この設定で、`vscode` 上で `python` ファイルを編集すると、ファイル保存時に自動で `black` のフォーマットが効いたり、コーディング中に `flake8` や `mypy` の違反があればエラーが出てくれます。

### extensions.json

先程 `.vscode/settings.json` について紹介しましたが、拡張機能が前提となっている設定も混ざっているので、`.vscode/extensions.json` も書いてあげると親切です。

```json:.vscode/extensions.json
{
  "recommendations": ["ms-python.python", "njpwerner.autodocstring"]
}
```
