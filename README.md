# subject_4-2-2_3

提出用課題 4-2-2 API連携実践課題 3. Gmail API


# Gmail API でメール送信（Python）

このプロジェクトは、Python から Gmail API を使ってメールを送信する最小構成のサンプルです。  
初回実行時はブラウザで Google ログインを行い、2回目以降は保存された `token.json` を使って認証します。

---

## 1. 環境構築

### 1-1. Python の準備

- Python 3.9 以上を推奨

バージョン確認:

```bash
python3 --version
```

### 1-2. 必要ライブラリをインストール

このプロジェクトには `requirements.txt` があるので、次のコマンドでまとめてインストールできます。

```bash
pip install -r requirements.txt
```

`requirements.txt` の内容:

- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`

---

## 2. Google Cloud 側の設定（簡単）

Gmail API を使うために、Google Cloud で最初に設定が必要です。

1. [Google Cloud Console](https://console.cloud.google.com/) を開く
2. 新しいプロジェクトを作成（または既存プロジェクトを選択）
3. 「API とサービス」→「ライブラリ」で **Gmail API** を有効化
4. 「API とサービス」→「OAuth 同意画面」を設定
   - テスト用なら「外部」で作成し、必要項目を入力
5. 「API とサービス」→「認証情報」→「認証情報を作成」→ **OAuth クライアント ID**
   - アプリの種類は「デスクトップアプリ」を選択
6. ダウンロードした JSON ファイルを、このプロジェクト直下に `credentials.json` という名前で配置

---

## 3. 実行方法

1. `gmail_send.py` を開く
2. `main()` 内の送信先や件名・本文を自分の値に変更
3. 次のコマンドで実行

```bash
python3 gmail_send.py
```

### 初回実行時

- ブラウザが起動し、Google ログイン・同意画面が表示されます
- 許可後、`token.json` が自動作成されます

### 2回目以降

- `token.json` を使って認証するため、通常はブラウザ認証が不要です

---

## 4. 注意点

- `credentials.json` と `token.json` は機密情報を含むため、外部に共有しないでください
- Git で管理する場合は、`credentials.json` と `token.json` を `.gitignore` に追加してください
- `SCOPES` を変更した場合、既存の `token.json` が使えないことがあります  
  その場合は一度 `token.json` を削除して再認証してください
- Gmail API の利用には Google Cloud 側の設定（API 有効化・OAuth 設定）が必須です

---

## 5. ファイル構成

- `gmail_send.py` : 認証処理とメール送信処理の本体
- `requirements.txt` : 必要ライブラリ一覧
- `credentials.json` : Google Cloud で発行した OAuth クライアント情報
- `token.json` : 実行後に生成される認証トークン
