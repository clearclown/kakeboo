# backend/image_process/reciept.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
from config import OPENAI_API_KEY, IMAGE_PATH
from image_utils import encode_image
from file_manager import select_image, move_processed_image
import os
import dotenv
import yaml
import logging
from datetime import datetime
import time

# [DEBUG] : デバッガーを初期化します
print("[DEBUG] : デバッガーを初期化しています...")

# ログ設定
log_folder = "./../log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, f"receipt_process_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# [DEBUG] : ログ設定が完了しました
print(f"[DEBUG] : ログ設定が完了しました。ログファイル: {log_file}")

dotenv.load_dotenv()

# [DEBUG] : 環境変数を読み込みました
print("[DEBUG] : 環境変数を読み込みました")

# 画像の選択と移動
SOURCE_FOLDER = "./../pics/02jpgpng/"
CURRENT_FOLDER = "./../pics/02currentPics/"
PROCESSED_FOLDER = "./../pics/02jpgpngdone/"
MD_OUTPUT_FOLDER = "./../pics/02currentMD/"

# [DEBUG] : フォルダパスを設定しました
print(f"[DEBUG] : フォルダパスを設定しました:\nSOURCE_FOLDER: {SOURCE_FOLDER}\nCURRENT_FOLDER: {CURRENT_FOLDER}\nPROCESSED_FOLDER: {PROCESSED_FOLDER}\nMD_OUTPUT_FOLDER: {MD_OUTPUT_FOLDER}")

# プロンプトの読み込み
try:
    with open('prompt.yml', 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
    # [DEBUG] : プロンプトを正常に読み込みました
    print("[DEBUG] : プロンプトを正常に読み込みました")
    logging.info("プロンプトを正常に読み込みました")
except Exception as e:
    # [DEBUG] : プロンプトの読み込みに失敗しました
    print(f"[DEBUG] : プロンプトの読み込みに失敗しました: {str(e)}")
    logging.error(f"プロンプトの読み込みに失敗しました: {str(e)}")
    raise

system_prompt = prompts['system']
human_prompt = prompts['human']

# [DEBUG] : ChatOpenAIインスタンスを初期化します
print("[DEBUG] : ChatOpenAIインスタンスを初期化しています...")
chat = ChatOpenAI(temperature=0, model_name="chatgpt-4o-latest")
# [DEBUG] : ChatOpenAIインスタンスの初期化が完了しました
print("[DEBUG] : ChatOpenAIインスタンスの初期化が完了しました")

# 画像がなくなるまで処理を繰り返す
while True:
    start_time = time.time()  # 処理開始時間を記録
    try:
        # [DEBUG] : 画像の選択を開始します
        print("[DEBUG] : 画像の選択を開始します...")
        # ランダムに画像を選択して移動
        IMAGE_PATH = select_image(SOURCE_FOLDER, CURRENT_FOLDER)
        # [DEBUG] : 画像の選択が完了しました
        print(f"[DEBUG] : 画像の選択が完了しました: {IMAGE_PATH}")
        logging.info(f"画像の選択が完了しました: {IMAGE_PATH}")
    except FileNotFoundError:
        # [DEBUG] : 処理する画像がなくなりました
        print("[DEBUG] : 処理する画像がなくなりました。プログラムを終了します。")
        logging.info("処理する画像がなくなりました。プログラムを終了します。")
        break

    try:
        # [DEBUG] : 画像のエンコードを開始します
        print("[DEBUG] : 画像のエンコードを開始します...")
        # 画像のエンコード
        base64_image, mime_type = encode_image(IMAGE_PATH)
        # [DEBUG] : 画像のエンコードが完了しました
        print("[DEBUG] : 画像のエンコードが完了しました")
        logging.info("画像のエンコードが完了しました")
    except Exception as e:
        # [DEBUG] : 画像のエンコードに失敗しました
        print(f"[DEBUG] : 画像のエンコードに失敗しました: {str(e)}")
        logging.error(f"画像のエンコードに失敗しました: {str(e)}")
        continue

    image_template = {"image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}

    # [DEBUG] : プロンプトの構築を開始します
    print("[DEBUG] : プロンプトの構築を開始します...")
    # プロンプトを構築してOpenAI APIに送信
    human_message_template = HumanMessagePromptTemplate.from_template([human_prompt, image_template])
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), human_message_template])
    # [DEBUG] : プロンプトの構築が完了しました
    print("[DEBUG] : プロンプトの構築が完了しました")

    # [DEBUG] : OpenAI APIにリクエストを送信します
    print("[DEBUG] : OpenAI APIにリクエストを送信します...")
    chain = prompt | chat
    try:
        result = chain.invoke("question")
        # [DEBUG] : OpenAI APIからの応答を受信しました
        print("[DEBUG] : OpenAI APIからの応答を受信しました")
        logging.info("OpenAI APIからの応答を受信しました")
    except Exception as e:
        # [DEBUG] : OpenAI APIリクエストに失敗しました
        print(f"[DEBUG] : OpenAI APIリクエストに失敗しました: {str(e)}")
        logging.error(f"OpenAI APIリクエストに失敗しました: {str(e)}")
        continue

    # [DEBUG] : 結果をMarkdownファイルとして保存します
    print("[DEBUG] : 結果をMarkdownファイルとして保存します...")
    # 結果をMarkdownファイルとして保存
    md_filename = os.path.join(MD_OUTPUT_FOLDER, os.path.basename(IMAGE_PATH).split('.')[0] + '.md')
    try:
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(f"```\n{result}\n```\n")
        # [DEBUG] : Markdownファイルの保存が完了しました
        print(f"[DEBUG] : Markdownファイルの保存が完了しました: {md_filename}")
        logging.info(f"Markdownファイルの保存が完了しました: {md_filename}")
    except Exception as e:
        # [DEBUG] : Markdownファイルの保存に失敗しました
        print(f"[DEBUG] : Markdownファイルの保存に失敗しました: {str(e)}")
        logging.error(f"Markdownファイルの保存に失敗しました: {str(e)}")
        continue

    # [DEBUG] : 処理済み画像の移動を開始します
    print("[DEBUG] : 処理済み画像の移動を開始します...")
    # 処理が完了した画像を移動
    try:
        move_processed_image(IMAGE_PATH, PROCESSED_FOLDER)
        # [DEBUG] : 処理済み画像の移動が完了しました
        print(f"[DEBUG] : 処理済み画像の移動が完了しました: {IMAGE_PATH} -> {PROCESSED_FOLDER}")
        logging.info(f"処理済み画像の移動が完了しました: {IMAGE_PATH} -> {PROCESSED_FOLDER}")
    except Exception as e:
        # [DEBUG] : 処理済み画像の移動に失敗しました
        print(f"[DEBUG] : 処理済み画像の移動に失敗しました: {str(e)}")
        logging.error(f"処理済み画像の移動に失敗しました: {str(e)}")
        continue

    end_time = time.time()  # 処理終了時間を記録
    processing_time = end_time - start_time  # 処理にかかった時間を計算

    # [DEBUG] : 画像処理が完了しました
    print(f"[DEBUG] : 画像処理が完了しました: {md_filename}")
    print(f"[DEBUG] : 処理にかかった時間: {processing_time:.2f}秒")
    logging.info(f"画像処理が完了しました: {md_filename}")
    logging.info(f"処理にかかった時間: {processing_time:.2f}秒")
