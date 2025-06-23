# 暦データAPI - Calendar Data API

日本の暦データを包括的に提供する無料のREST APIです。祝日、六曜、スピリチュアル要素など27項目のデータを2025年から2036年まで12年分提供します。

## 🌟 特徴

- **12年分のデータ**: 2025年〜2036年（計4383日）
- **27項目の豊富なデータ**: 基本情報からスピリチュアル要素まで
- **4つの形式対応**: JSON、CSV、XML、TXT
- **完全無料**: GitHub Pagesでホスト、CORS対応
- **レスポンシブ**: 全デバイス対応のドキュメントサイト

## 📡 API エンドポイント

### ベースURL
```
https://rei-abekura-lvgs.github.io/CalendarAPI/api/
```

### 月別データ
```
GET /api/{年}/{月}.{形式}
```

**例:**
- `/api/2025/01.json` - 2025年1月のJSONデータ
- `/api/2026/06.csv` - 2026年6月のCSVデータ
- `/api/2030/12.xml` - 2030年12月のXMLデータ
- `/api/2025/03.txt` - 2025年3月の読みやすいテキスト形式

### 年間データ
```
GET /api/{年}/all.{形式}
```

**例:**
- `/api/2025/all.json` - 2025年全データ（JSON）
- `/api/2026/all.csv` - 2026年全データ（CSV）

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

## 📋 データ項目説明（全27項目）

### 基本情報
| 項目 | 説明 |
|------|------|
| `day` | 日 |
| `date` | 日付（YYYY-MM-DD形式） |
| `weekday` | 曜日（日本語） |
| `weekday_en` | 曜日（英語） |
| `weekday_short` | 曜日（略語） |
| `is_weekend` | 週末かどうか |
| `is_holiday` | 祝日かどうか |
| `holiday_name` | 祝日名（祝日の場合） |

### 伝統暦
| 項目 | 説明 |
|------|------|
| `rokuyo` | 六曜（大安、友引、先勝、先負、赤口、仏滅） |
| `season_24` | 二十四節気 |
| `moon_phase` | 月の満ち欠け |

### スピリチュアル・ウェルネス
| 項目 | 説明 |
|------|------|
| `daily_keyword` | 今日のスピリチュアルキーワード |
| `color_of_the_day` | 今日の色（日本の伝統色名） |
| `recommended_tea` | おすすめのお茶 |
| `lucky_number` | ラッキーナンバー |
| `power_stone` | パワーストーン |
| `aroma_oil` | アロマオイル |
| `meditation_theme` | 瞑想テーマ |
| `flower_of_the_day` | 今日の花と花言葉 |
| `energy_advice` | エネルギーアドバイス |

### 占い・エンターテイメント
| 項目 | 説明 |
|------|------|
| `zodiac_influence` | 星座の影響 |
| `tarot_card` | タロットカード |
| `wise_quote` | 格言・名言 |
| `recommended_music` | おすすめ音楽ジャンル |
| `recommended_food` | おすすめ食事 |
| `crystal_healing` | クリスタルヒーリング |
| `feng_shui_tip` | 風水アドバイス |

## 使用例

### JavaScript
```javascript
// 今月のデータを取得
fetch('https://rei-abekura-lvgs.github.io/CalendarAPI/api/2025/06.json')
  .then(response => response.json())
  .then(data => {
    console.log('今月のデータ:', data);
    // 6月20日のデータを表示
    const day20 = data.days.find(d => d.day === 20);
    console.log(`今日のキーワード: ${day20.daily_keyword}`);
    console.log(`ラッキーナンバー: ${day20.lucky_number}`);
  });
```

### Python
```python
import requests

# 6月のデータを取得
response = requests.get('https://rei-abekura-lvgs.github.io/CalendarAPI/api/2025/06.json')
data = response.json()

# 特定の日のデータを取得
day_20 = next((day for day in data['days'] if day['day'] == 20), None)
if day_20:
    print(f"今日のキーワード: {day_20['daily_keyword']}")
    print(f"パワーストーン: {day_20['power_stone']}")
    print(f"風水アドバイス: {day_20['feng_shui_tip']}")
```

### cURL
```bash
# 最新の月データを取得
curl -X GET "https://rei-abekura-lvgs.github.io/CalendarAPI/api/2025/06.json" \
     -H "Accept: application/json"

# CSVファイルとしてダウンロード
curl -o "calendar_2025_06.csv" \
     "https://rei-abekura-lvgs.github.io/CalendarAPI/api/2025/06.csv"
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

## 🔄 更新履歴

- **2025-06-21**: 12年分データ生成完了（2025-2036年）
- **2025-06-21**: 27項目の包括的データ対応
- **2025-06-21**: レスポンシブデザイン完全対応
- **2025-06-20**: 複数形式対応（JSON、CSV、XML、TXT）
- **2025-06-20**: 初回リリース

## ⚙️ 技術仕様

- **ホスティング**: GitHub Pages
- **対象期間**: 2025年〜2036年（12年分）
- **総データ量**: 4383日分
- **データ形式**: 静的ファイル（JSON、CSV、XML、TXT）
- **レスポンス時間**: < 100ms
- **データサイズ**: 月別 ~25KB、年間 ~300KB（JSON形式）
- **CORS対応**: 全オリジンからアクセス可能

## 🔗 リンク

- **ドキュメントサイト**: https://rei-abekura-lvgs.github.io/CalendarAPI/
- **全ファイル一覧**: https://rei-abekura-lvgs.github.io/CalendarAPI/api_index.html
- **GitHubリポジトリ**: https://github.com/rei-abekura-lvgs/CalendarAPI

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

### 利用規約
- **教育・研究・個人利用**: 自由に利用可能
- **商用利用**: 可能（ただし正確性は保証されません）
- **データの信頼性**: 娯楽・参考目的での提供
- **重要な決定**: 専門家への相談を推奨

### 免責事項
- 四柱推命・占術データは娯楽・参考目的
- データ利用は自己責任でお願いします
- 重要な決定には専門家にご相談ください

詳細は [LICENSE](LICENSE) ファイルをご確認ください。

---

このAPIを使って素敵なアプリケーションを作ってください！