import os
import shutil
import logging
from PIL import Image

# ログ設定
import datetime
import os

# ログフォルダの作成
log_folder = "./log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
    print(f"\033[93m[DEBUG] : ログフォルダを作成しました: {log_folder}\033[0m")

# 現在の時刻を取得してファイル名に使用
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_folder, f"{current_time}_fileTo02jpgpng.log")

print(f"\033[93m[DEBUG] : ログファイル名: {log_file}\033[0m")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print(f"\033[93m[DEBUG] : ログ設定が完了しました\033[0m")

# ログファイルの作成を確認
if os.path.exists(log_file):
    print(f"\033[93m[DEBUG] : ログファイルが正常に作成されました: {log_file}\033[0m")
else:
    print(f"\033[93m[DEBUG] : ログファイルの作成に失敗しました\033[0m")

# デバッグ用の関数
def debug_print(message):
    print(f"\033[93m[DEBUG] : {message}\033[0m")

# フォルダのパスを指定
input_folder = "./pics/01notYet/"
output_folder = "./pics/02jpgpng/"

debug_print(f"入力フォルダ: {input_folder}")
debug_print(f"出力フォルダ: {output_folder}")

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    debug_print(f"出力フォルダを作成しました: {output_folder}")

# 入力フォルダ内の全てのファイルを取得
files = os.listdir(input_folder)
debug_print(f"入力フォルダ内のファイル数: {len(files)}")

for file in files:
    debug_print(f"処理中のファイル: {file}")
    file_path = os.path.join(input_folder, file)

    # ファイル名に全角または半角スペースがある場合、ハイフンに置き換える
    new_file_name = file.replace(' ', '-').replace('　', '-')
    new_file_path = os.path.join(input_folder, new_file_name)

    # 名前が変更された場合にファイルをリネーム
    if new_file_name != file:
        os.rename(file_path, new_file_path)
        logging.info(f'ファイル名 "{file}" を "{new_file_name}" に変更しました。')
        debug_print(f"ファイル名を変更しました: {file} -> {new_file_name}")
        file_path = new_file_path  # リネーム後のファイルパスを使用

    # 画像ファイルかどうか確認
    try:
        with Image.open(file_path) as img:
            img_format = img.format
            debug_print(f"画像フォーマット: {img_format}")

            # JPEGファイルで拡張子が間違っている場合
            if img_format == "JPEG" and new_file_name.lower().endswith('.heic'):
                correct_file = os.path.splitext(new_file_name)[0] + '.jpg'
                correct_path = os.path.join(output_folder, correct_file)
                shutil.move(file_path, correct_path)
                logging.info(f'{new_file_name} は JPEG形式でしたが、拡張子が .HEIC でした。{correct_file} に拡張子を修正して移動しました。')
                debug_print(f"JPEGファイルの拡張子を修正: {new_file_name} -> {correct_file}")

            # PNGファイルで拡張子が間違っている場合
            elif img_format == "PNG" and new_file_name.lower().endswith('.heic'):
                correct_file = os.path.splitext(new_file_name)[0] + '.png'
                correct_path = os.path.join(output_folder, correct_file)
                shutil.move(file_path, correct_path)
                logging.info(f'{new_file_name} は PNG形式でしたが、拡張子が .HEIC でした。{correct_file} に拡張子を修正して移動しました。')
                debug_print(f"PNGファイルの拡張子を修正: {new_file_name} -> {correct_file}")

            # すでに正しい拡張子がついている場合、そのまま移動
            elif new_file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                shutil.move(file_path, os.path.join(output_folder, new_file_name))
                logging.info(f'{new_file_name} をそのまま {output_folder} に移動しました。')
                debug_print(f"ファイルをそのまま移動: {new_file_name}")

            else:
                logging.warning(f'{new_file_name} はサポートされていない形式です。')
                debug_print(f"サポートされていない形式: {new_file_name}")

    except Exception as e:
        logging.error(f'{new_file_name} は画像ファイルではないか、エラーが発生しました: {e}')
        debug_print(f"エラー発生: {new_file_name}, エラー内容: {e}")

logging.info('処理が完了しました。')
debug_print("全ての処理が完了しました。")
