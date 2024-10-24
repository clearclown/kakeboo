# backend/image_process/file_manager.py

import os
import shutil
import random
import logging
from datetime import datetime

# ログの設定
log_folder = os.path.join(os.path.dirname(__file__), "..", "..", "log")
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, f"file_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def select_image(src_folder, dest_folder):
    print("[DEBUG] : select_image関数が呼び出されました。")
    logging.debug("select_image関数が呼び出されました。")

    # フォルダからランダムに1つの画像ファイルを選択
    print(f"[DEBUG] : ソースフォルダ: {src_folder}")
    print(f"[DEBUG] : 移動先フォルダ: {dest_folder}")
    logging.debug(f"ソースフォルダ: {src_folder}")
    logging.debug(f"移動先フォルダ: {dest_folder}")

    try:
        images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        print(f"[DEBUG] : 見つかった画像ファイル数: {len(images)}")
        logging.debug(f"見つかった画像ファイル数: {len(images)}")

        if not images:
            print("[DEBUG] : ソースフォルダに画像が見つかりませんでした。")
            logging.error("ソースフォルダに画像が見つかりませんでした。")
            raise FileNotFoundError("ソースフォルダに画像が見つかりませんでした。")

        selected_image = random.choice(images)
        print(f"[DEBUG] : 選択された画像: {selected_image}")
        logging.info(f"選択された画像: {selected_image}")

        src_path = os.path.join(src_folder, selected_image)
        dest_path = os.path.join(dest_folder, selected_image)

        # ファイルを移動
        print(f"[DEBUG] : 画像を移動します: {src_path} -> {dest_path}")
        logging.info(f"画像を移動します: {src_path} -> {dest_path}")
        shutil.move(src_path, dest_path)

        print(f"[DEBUG] : 画像の移動が完了しました。")
        logging.info("画像の移動が完了しました。")

        return dest_path  # 移動後の画像パスを返す

    except FileNotFoundError as e:
        print(f"[DEBUG] : エラー: {str(e)}")
        logging.error(f"エラー: {str(e)}")
        raise
    except Exception as e:
        print(f"[DEBUG] : 予期せぬエラーが発生しました: {str(e)}")
        logging.error(f"予期せぬエラーが発生しました: {str(e)}")
        raise

def move_processed_image(image_path, processed_folder):
    print("[DEBUG] : move_processed_image関数が呼び出されました。")
    logging.debug("move_processed_image関数が呼び出されました。")

    # 処理が完了した画像を別フォルダに移動
    print(f"[DEBUG] : 処理済み画像のパス: {image_path}")
    print(f"[DEBUG] : 移動先フォルダ: {processed_folder}")
    logging.debug(f"処理済み画像のパス: {image_path}")
    logging.debug(f"移動先フォルダ: {processed_folder}")

    try:
        dest_path = os.path.join(processed_folder, os.path.basename(image_path))
        print(f"[DEBUG] : 画像を移動します: {image_path} -> {dest_path}")
        logging.info(f"画像を移動します: {image_path} -> {dest_path}")

        shutil.move(image_path, dest_path)

        print(f"[DEBUG] : 処理済み画像の移動が完了しました。")
        logging.info("処理済み画像の移動が完了しました。")

    except FileNotFoundError as e:
        print(f"[DEBUG] : エラー: 指定された画像ファイルが見つかりません: {str(e)}")
        logging.error(f"エラー: 指定された画像ファイルが見つかりません: {str(e)}")
        raise
    except PermissionError as e:
        print(f"[DEBUG] : エラー: ファイルの移動権限がありません: {str(e)}")
        logging.error(f"エラー: ファイルの移動権限がありません: {str(e)}")
        raise
    except Exception as e:
        print(f"[DEBUG] : 予期せぬエラーが発生しました: {str(e)}")
        logging.error(f"予期せぬエラーが発生しました: {str(e)}")
        raise
