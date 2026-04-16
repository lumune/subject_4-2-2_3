import base64
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail送信に最低限必要なスコープ
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def authenticate_gmail_api(
    credentials_path: str = "credentials.json",
    token_path: str = "token.json",
):
    """
    Gmail APIクライアントを返す認証処理。
    - 初回実行: ブラウザでOAuth認証を行う
    - 2回目以降: 保存済み token.json を再利用する
    """
    # 認証情報を入れる変数。最初は何も入っていない状態。
    creds = None

    # 1) 以前の実行で保存した token.json があれば読み込む
    #    （アクセストークンとリフレッシュトークンが入っている）
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # 2) token.json がない / 無効な場合は認証をやり直す
    if not creds or not creds.valid:
        # 2-1) 有効期限切れでも refresh_token があれば自動更新できる
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 2-2) 初回実行時はこちらに入る
            # credentials.json を使ってOAuthフローを開始し、
            # ブラウザでGoogleアカウント認証を実施する
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # 3) 取得した認証情報を token.json に保存
        #    次回以降はこのファイルを使って再認証を省略できる
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    # 4) 認証済み credentials で Gmail API のサービスを作成して返す
    return build("gmail", "v1", credentials=creds)


def send_gmail_message(
    service,
    to_email: str,
    subject: str,
    body_text: str,
    user_id: str = "me",
):
    """
    Gmail APIでメールを送信する関数。
    宛先(to_email)、件名(subject)、本文(body_text)を指定できる。
    """
    # 1) MIMETextで本文をメール形式にする
    message = MIMEText(body_text, "plain", "utf-8")
    message["to"] = to_email
    message["subject"] = subject

    # 2) Gmail APIが受け取れるようにbase64(URL-safe)でエンコードする
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {"raw": raw}

    # 3) Gmail APIで送信する
    return service.users().messages().send(userId=user_id, body=body).execute()


def main():
    service = authenticate_gmail_api()

    to_email = input("宛先メールアドレスを入力してください: ").strip()
    subject = input("件名を入力してください: ").strip()
    body_text = input("本文を入力してください: ").strip()

    result = send_gmail_message(
        service=service,
        to_email=to_email,
        subject=subject,
        body_text=body_text,
    )

    print("送信完了:", result.get("id"))


if __name__ == "__main__":
    main()
