# Traffic Light Dataset - ToDayGAN 使用ガイド

## データセット概要
- **4つのドメイン**: Sunny Day (sd), Rainy Day (rd), Sunny Night (sn), Rainy Night (rn)
- **各ドメイン**: 300枚（訓練240枚 / テスト60枚）
- **合計**: 1200枚

## ステップ1: データセット準備

```bash
python3 prepare_traffic_dataset.py
```

実行後、以下のフォルダ構造が作成されます：
```
datasets/traffic_light_4domain/
├── train0/  # Sunny Day (訓練用: 240枚)
├── train1/  # Rainy Day (訓練用: 240枚)
├── train2/  # Sunny Night (訓練用: 240枚)
├── train3/  # Rainy Night (訓練用: 240枚)
├── test0/   # Sunny Day (テスト用: 60枚)
├── test1/   # Rainy Day (テスト用: 60枚)
├── test2/   # Sunny Night (テスト用: 60枚)
└── test3/   # Rainy Night (テスト用: 60枚)
```

## ステップ2: 訓練

### 方法1: スクリプトを使う（簡単）
```bash
bash scripts/train_traffic_light.sh
```

### 方法2: 直接pythonコマンドを使う（README通り）
```bash
python train.py \
    --name traffic_light_4domain \
    --dataroot ./datasets/traffic_light_4domain \
    --n_domains 4 \
    --niter 75 \
    --niter_decay 75 \
    --loadSize 512 \
    --fineSize 384
```

### パラメータ説明
- `--name`: 実験名（チェックポイント保存先）
- `--dataroot`: データセットのパス
- `--n_domains`: ドメイン数（今回は4）
- `--niter`: 学習率が一定のエポック数（75）
- `--niter_decay`: 学習率が減衰するエポック数（75）
- `--loadSize`: 画像を読み込む際のサイズ（512）
- `--fineSize`: ランダムクロップ後のサイズ（384）

### 追加オプション
- `--display_id 0`: visdomを使わない（デフォルトでは使用）
- `--gpu_ids 0`: GPU 0を使用（複数GPUの場合は `0,1,2`）
- `--gpu_ids -1`: CPUモード

チェックポイントは `./checkpoints/traffic_light_4domain/` に保存されます。

## ステップ3: 訓練の継続（Resume）

訓練を途中から再開する場合：
```bash
python train.py \
    --continue_train \
    --which_epoch 50 \
    --name traffic_light_4domain \
    --dataroot ./datasets/traffic_light_4domain \
    --n_domains 4 \
    --niter 75 \
    --niter_decay 75
```

## ステップ4: テスト

### 方法1: スクリプトを使う
```bash
bash scripts/test_traffic_light.sh
```

### 方法2: 直接pythonコマンドを使う（README通り）
```bash
python test.py \
    --phase test \
    --serial_test \
    --name traffic_light_4domain \
    --dataroot ./datasets/traffic_light_4domain \
    --n_domains 4 \
    --which_epoch 150
```

テスト結果は `./results/traffic_light_4domain/150/index.html` に保存されます。

## ドメイン変換の例

訓練後、以下のような変換が可能になります：
- Sunny Day → Rainy Day, Sunny Night, Rainy Night
- Rainy Day → Sunny Day, Sunny Night, Rainy Night
- Sunny Night → Sunny Day, Rainy Day, Rainy Night
- Rainy Night → Sunny Day, Rainy Day, Sunny Night

## 訓練の監視（オプション）

visdomを使って訓練を可視化する場合：
```bash
# 別のターミナルでvisdomサーバーを起動
python -m visdom.server

# ブラウザで http://localhost:8097 を開く
```

訓練時に `--display_id 1` を指定すると、visdomで損失やサンプル画像が表示されます。

## トラブルシューティング

### GPU メモリ不足の場合
```bash
# バッチサイズを減らす
python train.py ... --batchSize 1

# または画像サイズを小さくする
python train.py ... --loadSize 256 --fineSize 128
```

### 訓練時間の目安
- GPU使用: 1エポックあたり数分〜10分程度
- 150エポック: 数時間〜1日程度
