# Replitでのテスト方法ガイド

## 🧪 APIテストの実行方法

### 1. 自動テストツールの使用
```bash
python test_api.py
```

このツールが以下をテストします：
- 全エンドポイントの動作確認
- 今日のデータ取得
- 複数形式（JSON、CSV、XML、TXT）
- 複数年対応

### 2. 手動テスト方法

#### cURLでのテスト
```bash
# 基本テスト
curl http://localhost:5000/api/2025/06.json

# 今日のデータ
curl -s http://localhost:5000/api/2025/06.json | python -m json.tool

# CSVファイルテスト
curl http://localhost:5000/api/2025/01.csv

# 年間データ
curl http://localhost:5000/api/2025/all.json
```

#### ブラウザでのテスト
1. サーバーが動作中であることを確認（ポート5000）
2. 以下のURLにアクセス：
   - `http://localhost:5000/` - メインページ
   - `http://localhost:5000/api_index.html` - 全ファイル一覧
   - `http://localhost:5000/api/2025/06.json` - 6月データ

### 3. エラー対処法

#### 404エラーの場合
```bash
# ファイル存在確認
ls -la api/2025/

# サーバー再起動
# Replitワークフローを再起動
```

#### 今日のデータが表示されない場合
1. ブラウザの開発者ツールでJavaScriptエラーをチェック
2. ネットワークタブで404エラーを確認
3. `test_api.py`で詳細テスト実行

### 4. 開発時の注意点

#### Replit環境の特徴
- ポート5000が標準
- 相対パス（`./api/`）を使用
- ホットリロード対応
- 自動SSL（HTTPS）

#### 本番環境との違い
- Replit: `localhost:5000` または `*.replit.dev`
- 本番: `rei-abekura-lvgs.github.io/CalendarAPI`

### 5. デバッグのコツ

#### ログ確認
- ワークフローのコンソールログをチェック
- ブラウザの開発者ツールを活用
- `test_api.py`の詳細出力を確認

#### よくある問題
1. **クイックアクセス404**: URL自動判定で解決済み
2. **今日のデータ未表示**: JavaScript修正済み
3. **ファイル形式エラー**: Content-Type設定確認

## 🚀 デプロイ前チェックリスト

- [ ] 全エンドポイントが200を返す
- [ ] 今日のデータが正しく表示される
- [ ] レスポンシブデザインが動作する
- [ ] クイックアクセスリンクが機能する
- [ ] 全ファイル形式（JSON、CSV、XML、TXT）が利用可能