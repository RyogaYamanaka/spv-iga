import os
from pydub import AudioSegment

def merge_wav_files(input_folder, output_file):
    # フォルダ内のファイル名をアルファベット順に取得
    wav_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.wav')])
    
    # 音声を順に結合
    combined = AudioSegment.empty()
    for wav_file in wav_files:
        file_path = os.path.join(input_folder, wav_file)
        print(f"Adding {wav_file} from {input_folder}")
        audio = AudioSegment.from_wav(file_path)
        combined += audio
    
    # 結合したファイルを出力
    combined.export(output_file, format="wav")
    print(f"Combined audio saved as {output_file}")

# 入力フォルダと出力ファイルの対応をリストで設定
folders_and_outputs = [
    ('data/part/air', 'data/part/air.wav'),
    ('data/part/ear', 'data/part/ear.wav'),
    ('data/part/throat', 'data/part/throat.wav')
]

# 各フォルダに対して結合処理を実行
for input_folder, output_file in folders_and_outputs:
    merge_wav_files(input_folder, output_file)
