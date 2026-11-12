# ver1 形式の結果（result/<名前>/result_自己聴取音.txt など）を own/ と body/ に整理する補助スクリプト。
# ver4 の出力（param_own.txt など）には使わない。
import os
import shutil

def rename_and_move_files(result_folder, own_folder, body_folder):
    # own, body フォルダが存在しなければ作成
    os.makedirs(own_folder, exist_ok=True)
    os.makedirs(body_folder, exist_ok=True)

    # own/bodyフォルダの下にtxtフォルダとwavフォルダを作成
    own_txt_folder = os.path.join(own_folder, 'txt')
    own_wav_folder = os.path.join(own_folder, 'wav')
    body_txt_folder = os.path.join(body_folder, 'txt')
    body_wav_folder = os.path.join(body_folder, 'wav')

    os.makedirs(own_txt_folder, exist_ok=True)
    os.makedirs(own_wav_folder, exist_ok=True)
    os.makedirs(body_txt_folder, exist_ok=True)
    os.makedirs(body_wav_folder, exist_ok=True)

    # resultフォルダ内の各サブフォルダを処理
    for folder_name in os.listdir(result_folder):
        subfolder_path = os.path.join(result_folder, folder_name)
        
        # サブフォルダかどうか確認
        if os.path.isdir(subfolder_path):
            # サブフォルダ内のファイルをチェック
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)
                
                # result_自己聴取音.txt と 自己聴取音.wav を処理
                if filename == "result_自己聴取音.txt":
                    new_txt_name = folder_name + ".txt"
                    new_txt_path = os.path.join(own_txt_folder, new_txt_name)
                    shutil.move(file_path, new_txt_path)
                    print(f"Moved and renamed: {filename} -> {new_txt_name} to {own_txt_folder}")

                elif filename == "自己聴取音.wav":
                    new_wav_name = folder_name + ".wav"
                    new_wav_path = os.path.join(own_wav_folder, new_wav_name)
                    shutil.move(file_path, new_wav_path)
                    print(f"Moved and renamed: {filename} -> {new_wav_name} to {own_wav_folder}")

                # result_体内音.txt と 体内音.wav を処理
                elif filename == "result_体内音.txt":
                    new_txt_name = folder_name + ".txt"
                    new_txt_path = os.path.join(body_txt_folder, new_txt_name)
                    shutil.move(file_path, new_txt_path)
                    print(f"Moved and renamed: {filename} -> {new_txt_name} to {body_txt_folder}")

                elif filename == "体内音.wav":
                    new_wav_name = folder_name + ".wav"
                    new_wav_path = os.path.join(body_wav_folder, new_wav_name)
                    shutil.move(file_path, new_wav_path)
                    print(f"Moved and renamed: {filename} -> {new_wav_name} to {body_wav_folder}")

# 使用例: 実際のフォルダパスを指定
result_folder = 'result'  # resultフォルダへのパス
own_folder = 'own'        # ownフォルダへのパス
body_folder = 'body'      # bodyフォルダへのパス

rename_and_move_files(result_folder, own_folder, body_folder)
