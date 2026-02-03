# kaggle-template

Kaggleコンペティション用のテンプレートプロジェクト

## 環境構築

### 前提条件

- [uv](https://docs.astral.sh/uv/)

### 1. 環境変数の設定

```bash
# .env.example をコピー
cp .env.example .env

# .env を編集して Kaggle API の認証情報を設定
# https://www.kaggle.com/settings から API Token を作成
```

`.env` の内容：

```
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. 動作確認

```bash
# Kaggle CLIの確認
uv run kaggle competitions list

# 開発ツールの確認
uv run ruff --version
uv run pytest --version
uv run python --version
```

## 使い方

### データセットのダウンロード

```bash
# コンペティションのデータをダウンロード
uv run kaggle competitions download -c <competition-name>

# データセットのダウンロード
uv run kaggle datasets download -d <dataset-path>

# ダウンロードしたzipファイルを解凍
unzip <file>.zip -d data/
```

### コードのフォーマットとリント

```bash
# Ruffで自動フォーマット
uv run ruff format .

# Ruffでリント
uv run ruff check .

# 自動修正
uv run ruff check --fix .
```

### テストの実行

```bash
# すべてのテストを実行
uv run pytest

# カバレッジ付きで実行
uv run pytest --cov
```

### Jupyter Notebookの起動

```bash
# JupyterLabを起動
uv run jupyter lab --port=8888

# ブラウザで http://localhost:8888 にアクセス
```

## プロジェクト構造

```
.
├── data/                   # データセット（.gitignoreに含まれる）
├── notebooks/              # Jupyter Notebooks
├── outputs/                # 出力ファイル（学習済み重み、予測結果など）
├── scripts/                # 運用スクリプト
│   └── push_to_kaggle.py   # Kaggle へのカーネルプッシュ
├── src/                    # ソースコード
│   ├── models/             # モデル定義
│   ├── preprocessing/      # 前処理
│   ├── postprocessing/     # 後処理
│   ├── train.py            # 学習スクリプト
│   └── inference.py        # 推論スクリプト
├── templates/              # kernel-metadata.json のテンプレート
│   ├── kernel-metadata.train.template.json
│   └── kernel-metadata.inference.template.json
├── pyproject.toml          # プロジェクト定義・依存関係
└── uv.lock                 # ロックファイル（依存バージョン固定）
```

## インストール済みツール

### 開発ツール
- **Ruff**: 高速なPythonリンター/フォーマッター
- **pytest**: テストフレームワーク
- **mypy**: 静的型チェッカー
- **ipython**: 拡張対話型Python

### データサイエンス
- **pandas**: データ分析
- **numpy**: 数値計算
- **scikit-learn**: 機械学習
- **matplotlib/seaborn**: 可視化
- **XGBoost/LightGBM**: 勾配ブースティング

### Jupyter
- **jupyter**: Jupyter Notebook
- **jupyterlab**: JupyterLab

## Tips

### VS Code設定

保存時に自動的にRuffでフォーマットされます。

### Kaggle認証情報の更新

`.env` ファイルの `KAGGLE_USERNAME` と `KAGGLE_KEY` を更新してください。

### パッケージ管理（uv）

このプロジェクトではパッケージ管理に [uv](https://docs.astral.sh/uv/) を使用しています。
`pyproject.toml` で依存関係を定義し、`uv.lock` でバージョンを固定します。

#### パッケージの追加

```bash
# 通常の依存関係を追加
uv add <パッケージ名>

# バージョン指定で追加
uv add "polars>=0.20.0"

# 開発用ツールとして追加（dev グループ）
uv add --group dev <パッケージ名>
```

`uv add` を実行すると `pyproject.toml` への追記と `uv.lock` の更新が自動で行われます。

#### パッケージの削除

```bash
uv remove <パッケージ名>
```

#### 依存関係の同期

`uv.lock` の内容に基づいて環境を同期します。
他のメンバーの変更を取り込んだ後や、ロックファイルを更新した後に実行してください。

```bash
uv sync
```

#### ロックファイルの更新

`pyproject.toml` を手動で編集した場合はロックファイルを再生成してください。

```bash
uv lock
```

#### pip との対応表

| pip | uv |
|---|---|
| `pip install foo` + 手動で requirements.txt に追記 | `uv add foo` |
| `pip uninstall foo` + 手動で requirements.txt から削除 | `uv remove foo` |
| `pip freeze > requirements.txt` | `uv lock` |
| `pip install -r requirements.txt` | `uv sync` |
