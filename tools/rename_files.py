import os

def process_and_rename_files_in_folder(folder_path):
    # 指定したフォルダ内の全ファイルを処理
    for filename in os.listdir(folder_path):
        # ファイルが.wavで終わっている場合のみ処理
        if filename.endswith(".wav"):
            # 現在のファイルのフルパス
            old_file_path = os.path.join(folder_path, filename)
            
            # 末尾から4文字目のアルファベットと末尾2桁の数字を抽出
            base_name = filename[:-4]  # 拡張子を除いた部分
            new_filename = base_name[-4] + base_name[-2:] + ".wav"
            
            # 新しいファイルのフルパス
            new_file_path = os.path.join(folder_path, new_filename)
            
            # ファイルをリネーム
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")

# 使い方: python3 tools/rename_files.py <フォルダのパス>
# ファイル名（拡張子除く）の「末尾から4文字目 + 末尾2桁」に変える（例: air-01.wav → r01.wav）
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("python3 tools/rename_files.py <folder_path>")
        sys.exit(1)
    process_and_rename_files_in_folder(sys.argv[1])
