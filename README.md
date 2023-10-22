# ban-jinro-log-crawler

* python 3.8.1
* poerty 1.2.2

<br><br>

## Setup

### poetry

#### initialize

- poetry new xxxx  
  ※ ひな形が必要ない場合、poetry init で pyproject.toml のみ作成する。  
  ※ poetry はデフォルトでパッケージごとに仮想環境が作成される。  
     後続コマンドでは仮想環境上で実施されるので、venv と競合する場合 `python -m pip uninstall virtualenv` で venv を uninstall すること。  
  ※ 生成される xxxx フォルダを "src" に変更する。  
  ※ name / version / description は必須、authors は匿名にしておく必要があれば匿名にしておくこと。以下例  

```
name = "xxxx"
version = "0.1.0"
description = ""
authors = ["visualpaper"]
```

- poetry config virtualenvs.in-project true  
  ※ vscode との連携都合、仮想環境作成場所をフォルダ直下にします。

<b> env が読み込まれない事象が起きた場合は、キャッシュが問題なので clone し直して以下を実施すれば治る </b>

```
poetry config virtualenvs.in-project true  
poetry install
poetry run task start など
```

<br>

#### Formatter

- poetry add --group dev black  
  ※ コマンドは Task Runner 欄に記載する。  

- poetry add --group dev isort  
  ※ import の順番整合を整えてくれるもの。  

- poetry add --group dev autoflake  
  ※ 未使用な import を削除するためだけに利用している。  
  ※ デフォルトでは python 標準ライブラリのみが対象のため、必要に応じて imports を追加する必要がある。

```
[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88

[tool.autoflake]
imports = ["fastapi", "motor"] ← のように python 標準ライブラリ以外で必要に応じて追加すること。
```

<br>

#### Linter

- poetry add --group dev flake8  
  ※ コマンドは Task Runner 欄に記載する。  
  ※ flake8 が portry [未対応](https://github.com/PyCQA/flake8/issues/234) だが flake8 を使っている。  
  ※ python バージョンによって制限がかかることがあるため、以下のように version の指定を変更している。

```
[tool.poetry.dependencies]
python = ">=3.8.1"

[tool.flake8]
max-line-length = 88
```

<br>

#### Test

- poetry add --group dev pytest pytest-mock pytest-cov  
  ※ pytest-mock は mock 用、pytest-cov はカバレッジ表示用に入れています。  
  ※ src と tests フォルダがフラットに並んでいる場合 (src 配下に tests がない場合) 以下を toml ファイルに追加する必要があります。  
  ※ python 標準 unittest は原則利用が必要な場面でのみ利用する形で進めていますが、制限ではないです。

```
[tool.pytest.ini_options]
# tests が src と同階層にいる場合、tests から src を参照するために必要
pythonpath = [
  ".", "src"
]

[tool.coverage.report]
# pytest カバレッジ用の設定
## show_missing: test がない行を表示する (結果が長くなるのでデフォルトは false としています)
## skip_empty: 空ファイルを除外する (主に __init__.py 除外目的です)
show_missing = false
skip_empty = true
```

<br>

#### Task Runner

- poetry add --group dev taskipy  
  ※ python バージョンによって制限がかかることがあるため、以下のように version の指定を変更している。  
  ※ 以下を Task に追加する。  

```
[tool.poetry.dependencies]
python = ">=3.8.1,<4.0"
```

```
[tool.taskipy.tasks]
# skip-string-normalization で ' を " に変えることを抑制しています。
# ※ PEP8 では規定されていないが好みだと思うので抑制しています。
format = """\
         autoflake -r src tests --remove-all-unused-imports --in-place\
         && isort src tests\
         && black src tests --skip-string-normalization
         """

# max-line-length で black の定義 88 に合わせています。
# (参照) https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length
#
# W503 と E203 は black の定義と合わせています。
# (参照) https://rcmdnk.com/blog/2019/11/04/computer-python/
#        https://org-technology.com/posts/python-black.html
lint = "flake8 src tests --ignore=E203,W503 --max-line-length=88"

# -s: テスト実行中に print 文の出力を標準出力に書き出す。
# -v: テストごとの Success/Failed を表示する。
# --cov: カバレッジを表示する。
test = "pytest tests -s -vv --cov"
```

<br><br>

### VSCode

#### extensions

以下、VSCode 拡張をインストールする。

```
    "recommendations": [
        // https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance
        "ms-python.vscode-pylance",
        // https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter
        "ms-python.black-formatter",
        // https://marketplace.visualstudio.com/items?itemName=ms-python.flake8
        "ms-python.flake8",
    ]
```

<br>

#### defaultInterpreterPath

CTRL + SHIFT + P で「Python Select Interpreter」を選択し Poetry にて作成された venv の場所を指定すること。  
※ こうしないと Global (/home/python など) の場所を見て import などの解決がされてしまうためコンパイルができない。

<br>

#### formatter

- black  
  ※ PEP8 準拠していない場合など自動修正してくれるようになる。

```
    // formatter
    // 以下に沿って、VSCode 拡張をインストールする。
    // https://github.com/microsoft/vscode-python/wiki/Migration-to-Python-Tools-Extensions
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
    },
    "black-formatter.args": [
        // skip-string-normalization で ' を " に変えることを抑制している。
        // # ※ PEP8 では規定されていないが好みだと思うので抑制している。
        "skip-string-normalization"
    ],
```

<br>

#### linter

- flake8

```
    // linter
    // 以下に沿って、VSCode 拡張をインストールする。
    // https://github.com/microsoft/vscode-python/wiki/Migration-to-Python-Tools-Extensions
    "flake8.args": [
        // black の定義 88 に合わせています。
        // (参照) https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length
        "--max-line-length=88",
        // W503 と E203 は black の定義と合わせています。
        // (参照) https://rcmdnk.com/blog/2019/11/04/computer-python/
        //        https://org-technology.com/posts/python-black.html
        "--ignore=E203,W503"
    ],
```

※ PEP8 準拠していない場合など警告が出るようになる。

<br>

#### type hints

- Pylance  
  ※ 入力補完、自動インポートなど。  

```
    // Pylance 拡張機能での型チェックを行うようにする。
    "python.analysis.typeCheckingMode": "basic"
```

<br><br>

### Library

#### pydantic

- poetry add pydantic  
  ※ 型ヒントを元に Validation を行うために必要  
  ※ Pylance は静的解析レベルで、pydantic は型を元に Validation エラーまで出してくれる。    

- poetry add pydantic-settings  
  ※ Env から設定を読み込む際に利用している。  
  ※ 元々 pydantic V1 では不要だったが V2 から別途必要になったので入れている。

<br>

#### Env

- poetry add python-dotenv  
  ※ 開発時には .env ファイルを利用する。  
  ※ テスト時には Setting を override する。  
  ※ デプロイ時には環境変数を指定して override する。  
  ※ gitignore より `.env` を対象にするよう変更すること。

```
# Environments
#.env ← をコメントアウトし commit 対象とすること。
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

<br>

#### Inject

- poetry add injector  
  (参照) https://injector.readthedocs.io/en/latest/index.html  
  ※ フレームワークに搭載されている DI 機能を利用できるなら、そちらのほうが良いと思っている。

<br>

### Rest Client

- poetry add requests  
  ※ Scraping を行うために必要。

<br>

### Parser

- poetry add beautifulsoup4  
  ※ Scraping を行うために必要。

<br>

### MongoDB

- poetry add pymongo  
  (参照) https://pymongo.readthedocs.io/en/stable/index.html

- poetry add --group dev mongomock  
  ※ mongodb mock 用に入れている。  
  (参照) https://docs.mongoengine.org/index.html

```
MongoDB Atlas (https://www.mongodb.com/atlas/database) 無料枠を利用

Provider: AWS
Region: Tokyo (ap-northeast-1)
DB Cluster: ban-jinro-log-cluster
DB: ban-jinro-log-db
Collection
  - td_village
    - Index:
      - { "villageNumber": 1 }, { unique: true }
  - tw_latest_crawled
    ※ 事前に 1 レコードを登録し、1 レコードがある前提で動作させている。
    > {"_id":{"$oid":"6534bebb95d323df1bfafaee"},"value":{"$numberInt":"2"}}
```

<br><br>

## Build

- poetry install
- poetry run task format
- poetry run task lint
- poetry run task test
- poetry run task start
