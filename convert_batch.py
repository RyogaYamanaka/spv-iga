import os
import glob
import convert_sound

# デフォルトのパラメータ
f_border = [31, 44, 63, 88, 125, 180, 250, 355, 500, 710, 1000, 1400, 2000, 2800, 4000, 5600, 8000, 11300, 16000, 22000]
air_folder = 'data/all/air'   # 気導音のフォルダ
ear_folder = 'data/all/ear'   # 耳骨導音のフォルダ
throat_folder = 'data/all/throat'  # 喉骨導音のフォルダ
output_folder_body = 'data/all/body'  # 体内音の出力フォルダ
output_folder_myvoice = 'data/all/own'  # 自己聴取音の出力フォルダ
body_params = 'data/all/param_body.txt'  # 体内音のパラメータファイル
myvoice_params = 'data/all/param_own.txt'  # 自己聴取音のパラメータファイル

# 必要なディレクトリを作成
os.makedirs(output_folder_body, exist_ok=True)
os.makedirs(output_folder_myvoice, exist_ok=True)

def process_audio_files(air_folder, ear_folder, throat_folder, output_folder_body, output_folder_myvoice, body_params, myvoice_params):
    try:
        # 各フォルダ内の.wavファイルをアルファベット順で取得
        air_files = sorted(glob.glob(os.path.join(air_folder, "*.wav")))
        ear_files = sorted(glob.glob(os.path.join(ear_folder, "*.wav")))
        throat_files = sorted(glob.glob(os.path.join(throat_folder, "*.wav")))

        # 各フォルダにファイルが存在するか確認
        if not air_files or not ear_files or not throat_files:
            raise FileNotFoundError("エラー：選択されたフォルダに.wavファイルが見つかりませんでした。")

        # ファイルをループして変換を実行
        for air_file, ear_file, throat_file in zip(air_files, ear_files, throat_files):
            file_name = os.path.basename(air_file)  # ファイル名を取得
            print(f"{file_name}を処理中...")

            # convert_soundモジュールを使用して変換を実行
            try:
                convert_sound.conversion(f_border, air_file, ear_file, throat_file, body_params, myvoice_params, output_folder_body, output_folder_myvoice, file_name)
                print(f"{file_name}の処理に成功しました。")
            except Exception as e:
                print(f"{file_name}の変換中にエラーが発生しました: {e}")
                continue  # エラー時は次のファイルに進む

        print("全ファイルの処理が完了しました。")

    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

# 処理を開始
process_audio_files(air_folder, ear_folder, throat_folder, output_folder_body, output_folder_myvoice, body_params, myvoice_params)
