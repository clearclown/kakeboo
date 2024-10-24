# backend/process/config.py

import os
import logging
from dotenv import load_dotenv

print("[DEBUG] : configファイルの処理を開始します。")

# ログの設定
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'config.log'), level=logging.DEBUG)

print("[DEBUG] : ログの設定が完了しました。")
logging.debug("ログの設定が完了しました。")

try:
    print("[DEBUG] : .envファイルの読み込みを開始します。")
    load_dotenv()
    print("[DEBUG] : .envファイルの読み込みが完了しました。")
    logging.debug(".envファイルの読み込みが完了しました。")
except Exception as e:
    print(f"[DEBUG] : .envファイルの読み込み中にエラーが発生しました: {str(e)}")
    logging.error(f".envファイルの読み込み中にエラーが発生しました: {str(e)}")

# APIキーの設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    print("[DEBUG] : OpenAI APIキーの設定が完了しました。")
    logging.debug("OpenAI APIキーの設定が完了しました。")
else:
    print("[DEBUG] : OpenAI APIキーが設定されていません。")
    logging.warning("OpenAI APIキーが設定されていません。")

# 画像パスの設定（ここで動的に設定される）
IMAGE_PATH = ""
print("[DEBUG] : 画像パスの初期化が完了しました。")
logging.debug("画像パスの初期化が完了しました。")

print("[DEBUG] : configファイルの処理が完了しました。")
logging.debug("configファイルの処理が完了しました。")
