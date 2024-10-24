# backend/process/image_utils.py

from PIL import Image
import base64
import io
import os
import logging
import datetime

# ログ設定
log_dir = "./../log"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"image_utils_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image(image_path):
    print("[DEBUG] : encode_image関数が呼び出されました。")
    logging.debug("encode_image関数が呼び出されました。")

    try:
        # Pillowを使って画像を開く
        print(f"[DEBUG] : 画像を開こうとしています: {image_path}")
        logging.debug(f"画像を開こうとしています: {image_path}")
        img = Image.open(image_path)
        print("[DEBUG] : 画像の開封に成功しました。")
        logging.debug("画像の開封に成功しました。")

        # 画像形式を判定し、適切なMIMEタイプを設定
        print("[DEBUG] : 画像形式を判定しています。")
        logging.debug("画像形式を判定しています。")
        if img.format == 'JPEG':
            mime_type = 'image/jpeg'
            print("[DEBUG] : JPEG形式が検出されました。")
            logging.debug("JPEG形式が検出されました。")
        elif img.format == 'PNG':
            mime_type = 'image/png'
            print("[DEBUG] : PNG形式が検出されました。")
            logging.debug("PNG形式が検出されました。")
        else:
            print(f"[DEBUG] : サポートされていない画像形式です: {img.format}")
            logging.error(f"サポートされていない画像形式です: {img.format}")
            raise ValueError(f"サポートされていない画像形式です: {img.format}")

        # 画像をメモリバッファに保存
        print("[DEBUG] : 画像をメモリバッファに保存しています。")
        logging.debug("画像をメモリバッファに保存しています。")
        buffered = io.BytesIO()
        img.save(buffered, format=img.format)
        print("[DEBUG] : 画像のメモリバッファへの保存が完了しました。")
        logging.debug("画像のメモリバッファへの保存が完了しました。")

        # バッファの内容をbase64エンコード
        print("[DEBUG] : バッファの内容をbase64エンコードしています。")
        logging.debug("バッファの内容をbase64エンコードしています。")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        print("[DEBUG] : base64エンコードが完了しました。")
        logging.debug("base64エンコードが完了しました。")

        print("[DEBUG] : encode_image関数が正常に完了しました。")
        logging.debug("encode_image関数が正常に完了しました。")
        return img_str, mime_type

    except FileNotFoundError as e:
        print(f"[DEBUG] : ファイルが見つかりません: {image_path}")
        logging.error(f"ファイルが見つかりません: {image_path}")
        raise FileNotFoundError(f"ファイルが見つかりません: {image_path}") from e

    except IOError as e:
        print(f"[DEBUG] : 画像の読み込み中にエラーが発生しました: {e}")
        logging.error(f"画像の読み込み中にエラーが発生しました: {e}")
        raise IOError(f"画像の読み込み中にエラーが発生しました: {e}") from e

    except Exception as e:
        print(f"[DEBUG] : 予期せぬエラーが発生しました: {e}")
        logging.error(f"予期せぬエラーが発生しました: {e}")
        raise Exception(f"予期せぬエラーが発生しました: {e}") from e
