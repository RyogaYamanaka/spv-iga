# spv-iga：IGA による自己聴取音（SPV）推定システム

気導音・耳（外耳道内壁振動）音・喉骨導音の 3 信号から、被験者本人の主観評価をもとに対話型遺伝的アルゴリズム（IGA）でフィルタと重みを最適化し、体内音と自己聴取音（Self-Perceived Voice; SPV）を推定する Kivy 製の GUI アプリである。旧「IGAシステム ver4」を整理したもの。

- ① **推定**（`main.py`）：3 信号から体内音 → 自己聴取音の順にパラメータを決め、`own.wav` と `param_own.txt` を得る。1 人 15〜20 分程度。
- ② **一括変換**（`convert_batch.py`）：①で得たパラメータを使い、別の録音をまとめて体内音・自己聴取音に変換する。

## フォルダ構成

```
spv-iga/
├── main.py              # ① 推定アプリ本体（python3 main.py）
├── GA.py                # 評価値から次世代の 8 候補を作る
├── gen_sound.py         # パラメータから候補音声を生成・結果を保存
├── my.kv                # ① の画面定義
├── convert_batch.py     # ② 一括変換（旧 main2_improverd.py）
├── convert_sound.py     # ② の変換処理
├── font/                # アプリ用フォント（Noto Sans JP）
├── data/                # 入出力の置き場所（中身は git 管理外）
│   ├── part/{air,ear,throat}/   # ① 用の短い発話（結合前）
│   └── all/{air,ear,throat}/    # ② で変換したい録音
├── tools/               # 補助スクリプト
│   ├── merge_wav_file.py        # data/part/*/ の wav を結合して air.wav などを作る
│   ├── to_monoral.py            # ステレオ → モノラル
│   ├── normalize.py             # 音量の正規化
│   ├── melcp.py                 # 2 音声のメルケプストラム歪み（評価用）
│   ├── rename_files.py          # ファイル名の一括変更
│   └── organize_results_ver1.py # ver1 形式の結果整理（ver4 では不要）
├── requirements.txt
└── requirements-eval.txt  # tools/melcp.py を使うときだけ
```

## 環境構築

**Python 3.7 が必要**である。requirements.txt が numpy==1.18.1・numba==0.48.0 を固定しており、Python 3.7.4 で動作を確認している。3.10 では動かない。

```bash
# conda の例（pyenv + venv でもよい）
conda create -n iga python=3.7.4
conda activate iga
cd spv-iga
pip install -r requirements.txt
```

Apple Silicon の Mac では Python 3.7 のネイティブ版がないため、Rosetta 上の Intel 版環境を作る（未検証）。

```bash
CONDA_SUBDIR=osx-64 conda create -n iga python=3.7.4
conda activate iga
conda config --env --set subdir osx-64
pip install -r requirements.txt
```

## 使い方① SPV を推定する（main.py）

### 入力の条件

- 3 信号（air / ear / throat）は **同じ発話を同じ区間で切り出した、モノラルの wav**。長さが少しでも違う、ステレオ、wav 以外のいずれでもアプリが落ちることがある。ステレオは `tools/to_monoral.py` で変換する。
- ファイルは **このフォルダの中** に置く。ファイル選択画面はこのフォルダより上を参照できない。
- 既定では `data/part/air.wav`・`ear.wav`・`throat.wav` を読む。短い発話が複数あるときは `data/part/air/` などに並べて結合する。

```bash
python3 tools/merge_wav_file.py   # data/part/{air,ear,throat}/ → data/part/{air,ear,throat}.wav
```

### 手順

1. このフォルダで `python3 main.py` を実行する（候補音声を実行フォルダに書き出すので、必ずこのフォルダで実行する）。
2. 「気導音を選択」「耳骨導音を選択」「喉骨導音を選択」で 3 ファイルを指定し、「選択完了 音源評価に進む」を押す。約 20 秒で候補ができる。
3. **体内音の評価（イヤーマフ着用）**：体内音 1〜8 をすべて聞き、1〜5 で評価して OK。8 個の中で最も近いものを 5、最も遠いものを 1 にする。8 個すべて評価しないと次の世代に進まない。
4. 納得のいく候補が出るまで 3 を繰り返す（目安 4 世代、15〜20 分）。
5. 「体内音完成」で最も良い番号を選ぶ。`body.wav` と `param_body.txt` が保存され、自己聴取音の評価に移る。
6. **自己聴取音の評価（イヤーマフを外す）**：同じように評価を繰り返し、最後に最も良い番号を選んで終了する。`own.wav`（推定した SPV）と `param_own.txt` が保存され、アプリが閉じる。

出力先は、気導音ファイルを選んだフォルダ（選ばなければ `data/`）である。

### IGA が探索するもの

| 項目 | 内容 |
| --- | --- |
| フィルタ（各信号 1 つ） | ローパス。20 帯域の境界（31 Hz〜22 kHz）から減衰開始・終了の 2 点を選び、その間を対数周波数上で 0 → −48 dB に下げる。ランダム生成では開始 180〜2800 Hz、終了 4000 Hz まで |
| 体内音の重み | α（気導）、β（耳）、1−α−β（喉） |
| 自己聴取音の重み | γ（体内音）、1−γ（フィルタなしの気導音） |
| 1 世代 | 8 候補 = エリート 1・ルーレット 1・BLX 交叉 2（拡張率 1.5）・ランダム 4。第 1 世代は全てランダム |
| 第 2 段階 | フィルタと体内音の重みを第 1 段階の結果で固定し、γ だけを探索 |

重み w は 10^(0.5 × log2 w) で振幅に変換してから混ぜている。`param_*.txt` の重みは振幅比そのものではない。

## 使い方② 同じパラメータで他の録音を変換する（convert_batch.py）

1. `data/all/air`・`data/all/ear`・`data/all/throat` に各信号の wav を入れる。ファイル名順で 3 信号が対応づけられるので、名前をそろえる。
2. ①で得た `param_body.txt` と `param_own.txt` を `data/all/` に置く。
3. `python3 convert_batch.py` を実行する。`data/all/body/` と `data/all/own/` に変換後の音声が出る。

変換したい発話すべてに 3 信号の録音が必要である。気導音だけの音声を SPV の声質にしたいときは、`own.wav` を参照音声にして声質変換（KANADE など）を使う。

## 既知の問題

- 評価の途中で音声出力装置（イヤホン ↔ スピーカー）を切り替えられない。起動前に出力先を決めておく。
- `normalize()` は最大値で割るだけなので、無音や負のピークが大きい音声では想定どおりにならないことがある。

## バージョンの経緯

| 版 | 内容 |
| --- | --- |
| ver1 | 体内音と自己聴取音を個別に推定 |
| ver2 | 体内音を推定し、6 つの重みセットから自己聴取音を選ぶ |
| ver3 | ver1 から喉骨導音を除いたもの（削除済み） |
| **ver4（本リポジトリ）** | 体内音を推定し、そのパラメータを引き継いで自己聴取音の重みも IGA で推定 |
| ver5 | ver4 から喉骨導音を除いたもの |

## 参考文献

- R. Chen et al., Proc. APSIPA ASC, 821–828, 2021.
- 田中他, 日本音響学会研究発表会講演論文集, 2022.
- R. Yamanaka et al., Proc. SLaTE, 209–213, 2025.
