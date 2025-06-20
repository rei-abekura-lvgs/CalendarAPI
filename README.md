# 日本暦API - Japanese Calendar API

2025年の日本暦データを提供する無料のREST APIです。祝日、六曜、今日のキーワード、おすすめのお茶、今日の色などの情報を複数の形式で取得できます。

## API エンドポイント

### ベースURL
```
https://[ユーザー名].github.io/[リポジトリ名]/api/2025/
```

### 月別データ
```
GET /api/2025/{月}.{形式}
```

**例:**
- `/api/2025/01.json` - 1月のJSONデータ
- `/api/2025/06.csv` - 6月のCSVデータ
- `/api/2025/12.xml` - 12月のXMLデータ
- `/api/2025/03.txt` - 3月の読みやすいテキスト形式

### 年間データ
```
GET /api/2025/all.{形式}
```

**例:**
- `/api/2025/all.json` - 2025年全データ（JSON）
- `/api/2025/all.csv` - 2025年全データ（CSV）

## 対応形式

| 形式 | 説明 | Content-Type |
|------|------|--------------|
| JSON | プログラム利用に最適 | application/json |
| CSV | Excel等での利用に最適 | text/csv |
| XML | システム間連携に最適 | application/xml |
| TXT | 人間が読みやすい形式 | text/plain |

## データ構造（JSON）

```json
{
  "year": 2025,
  "month": 6,
  "month_name": "June",
  "month_name_jp": "6月",
  "api_version": "v1",
  "generated_at": "2025-06-20T08:45:25.831680",
  "days": [
    {
      "day": 20,
      "date": "2025-06-20",
      "weekday": "金曜日",
      "weekday_en": "Friday",
      "weekday_short": "Fri",
      "is_weekend": false,
      "is_holiday": false,
      "holiday_name": null,
      "rokuyo": "先勝",
      "season_24": null,
      "moon_phase": "調査中",
      "daily_keyword": "内なる光が輝く",
      "color_of_the_day": "黄金色",
      "recommended_tea": "ジャスミンティー"
    }
  ]
}
```

## データ項目説明

| 項目 | 説明 |
|------|------|
| `date` | 日付（YYYY-MM-DD形式） |
| `weekday` | 曜日（日本語） |
| `weekday_en` | 曜日（英語） |
| `is_weekend` | 週末かどうか |
| `is_holiday` | 祝日かどうか |
| `holiday_name` | 祝日名（祝日の場合） |
| `rokuyo` | 六曜（大安、友引、先勝、先負、赤口、仏滅） |
| `daily_keyword` | 今日のスピリチュアルキーワード |
| `color_of_the_day` | 今日の色（日本の伝統色名） |
| `recommended_tea` | おすすめのお茶 |

## 使用例

### JavaScript
```javascript
// 今月のデータを取得
fetch('https://[your-username].github.io/[repo-name]/api/2025/06.json')
  .then(response => response.json())
  .then(data => {
    console.log('今月のデータ:', data);
  });
```

### Python
```python
import requests

# 6月のデータを取得
response = requests.get('https://[your-username].github.io/[repo-name]/api/2025/06.json')
data = response.json()
print(f"今日のキーワード: {data['days'][19]['daily_keyword']}")
```

### CSV（Excel等）
CSVファイルを直接ダウンロードしてExcelで開くことができます。

## 特徴

- **完全無料**: GitHub Pagesでホストされており、使用料は一切かかりません
- **CORS対応**: ブラウザから直接アクセス可能
- **複数形式**: JSON、CSV、XML、TXT形式に対応
- **スピリチュアル要素**: 毎日のキーワードや色で運勢を楽しめます
- **日本文化**: 六曜や日本の伝統色を使用

## ライセンス

このAPIは自由に利用できます。商用・非商用問わずご利用ください。

## 更新履歴

- 2025-06-20: 初回リリース
- 複数形式対応（JSON、CSV、XML、TXT）
- スピリチュアルキーワード機能
- 日本の伝統色対応

## 技術仕様

- **ホスティング**: GitHub Pages
- **データ形式**: 静的ファイル
- **更新頻度**: 年1回（翌年データ追加）
- **レスポンス時間**: < 100ms
- **データサイズ**: 月別 ~13KB、年間 ~150KB（JSON形式）

---

このAPIを使って素敵なアプリケーションを作ってください！