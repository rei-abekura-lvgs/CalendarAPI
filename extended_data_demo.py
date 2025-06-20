#!/usr/bin/env python3
import json
import random
from datetime import datetime

def show_extended_data_sample():
    """拡張されたデータのサンプルを表示"""
    print("=== 日本暦API 拡張データサンプル ===\n")
    
    # 今日のデータを表示
    with open('api/2025/06.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today_data = data['days'][19]  # 6月20日
    
    print(f"📅 {today_data['date']} ({today_data['weekday']})")
    print(f"📜 六曜: {today_data['rokuyo']}")
    print()
    
    print("🌟 スピリチュアル情報:")
    print(f"  キーワード: {today_data['daily_keyword']}")
    print(f"  ラッキーナンバー: {today_data['lucky_number']}")
    print(f"  パワーストーン: {today_data['power_stone']}")
    print(f"  エネルギーアドバイス: {today_data['energy_advice']}")
    print()
    
    print("🎨 美と癒し:")
    print(f"  今日の色: {today_data['color_of_the_day']}")
    print(f"  今日の花: {today_data['flower_of_the_day']}")
    print(f"  アロマオイル: {today_data['aroma_oil']}")
    print()
    
    print("🧘 ウェルネス:")
    print(f"  瞑想テーマ: {today_data['meditation_theme']}")
    print(f"  おすすめのお茶: {today_data['recommended_tea']}")
    print()
    
    # ランダムに他の日も表示
    print("🎲 他の日のサンプル:")
    random_days = random.sample(data['days'], 3)
    for day in random_days:
        print(f"\n📅 {day['date']}:")
        print(f"  {day['daily_keyword']} | 🔮{day['power_stone']} | 🌸{day['flower_of_the_day']}")

def show_data_categories():
    """提供データのカテゴリ一覧"""
    print("\n=== 提供データカテゴリ ===\n")
    
    categories = {
        "📅 基本暦情報": [
            "日付・曜日", "週末判定", "祝日情報", "祝日名"
        ],
        "🏮 日本文化": [
            "六曜（大安・友引等）", "二十四節気（今後対応）", "月の満ち欠け（今後対応）"
        ],
        "🌟 スピリチュアル": [
            "今日のキーワード", "ラッキーナンバー", "パワーストーン", "エネルギーアドバイス"
        ],
        "🎨 美と癒し": [
            "今日の色（日本伝統色）", "今日の花と花言葉", "アロマオイル"
        ],
        "🧘 ウェルネス": [
            "瞑想テーマ", "おすすめのお茶"
        ],
        "📊 データ形式": [
            "JSON（API連携）", "CSV（Excel等）", "XML（システム統合）", "TXT（人間用）"
        ]
    }
    
    for category, items in categories.items():
        print(f"{category}:")
        for item in items:
            print(f"  • {item}")
        print()

if __name__ == "__main__":
    show_extended_data_sample()
    show_data_categories()
    
    print("=== 追加可能なデータ例 ===")
    print("🎯 占星術: 星座、惑星の位置")
    print("🎴 タロット: 今日のカード") 
    print("🌙 月齢: 正確な月相情報")
    print("🌸 季節: 二十四節気、七十二候")
    print("🍜 料理: 今日のおすすめレシピ")
    print("📚 名言: 今日の格言・名言")
    print("🎵 音楽: 気分に合う楽曲ジャンル")
    print("🌍 天候: 運勢に合わせた服装アドバイス")