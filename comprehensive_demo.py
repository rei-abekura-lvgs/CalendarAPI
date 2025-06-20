#!/usr/bin/env python3
import json
import random

def show_comprehensive_data():
    """拡張された全データカテゴリのデモ"""
    print("=== 日本暦API 完全版データカテゴリ ===\n")
    
    with open('api/2025/06.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today_data = data['days'][19]  # 6月20日
    
    print(f"📅 {today_data['date']} ({today_data['weekday']})")
    print("=" * 50)
    
    # カテゴリ別に整理して表示
    categories = {
        "📅 基本暦情報": {
            "六曜": today_data['rokuyo'],
            "祝日": today_data['holiday_name'] or "平日"
        },
        "🌟 スピリチュアル": {
            "今日のキーワード": today_data['daily_keyword'],
            "ラッキーナンバー": today_data['lucky_number'],
            "パワーストーン": today_data['power_stone'],
            "エネルギーアドバイス": today_data['energy_advice']
        },
        "🎴 占い・神秘": {
            "星座の影響": today_data['zodiac_influence'],
            "タロットカード": today_data['tarot_card'],
            "クリスタルヒーリング": today_data['crystal_healing']
        },
        "🎨 美と癒し": {
            "今日の色": today_data['color_of_the_day'],
            "今日の花": today_data['flower_of_the_day'],
            "アロマオイル": today_data['aroma_oil']
        },
        "🧘 ウェルネス": {
            "瞑想テーマ": today_data['meditation_theme'],
            "おすすめのお茶": today_data['recommended_tea'],
            "推奨音楽": today_data['recommended_music']
        },
        "🍽️ ライフスタイル": {
            "おすすめ食材": today_data['recommended_food'],
            "風水アドバイス": today_data['feng_shui_tip']
        },
        "💭 精神性": {
            "今日の格言": today_data['wise_quote']
        }
    }
    
    for category, items in categories.items():
        print(f"\n{category}:")
        for key, value in items.items():
            print(f"  {key}: {value}")
    
    print(f"\n📊 データ項目数: {len([k for k in today_data.keys() if k not in ['day', 'date', 'weekday_en', 'weekday_short', 'is_weekend', 'is_holiday', 'season_24', 'moon_phase']])}項目")

def show_random_samples():
    """他の日のランダムサンプル"""
    print("\n\n=== 他の日のサンプル ===")
    
    with open('api/2025/06.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sample_days = random.sample(data['days'], 3)
    
    for day in sample_days:
        print(f"\n📅 {day['date']}:")
        print(f"  {day['daily_keyword']} | {day['tarot_card']}")
        print(f"  {day['power_stone']} | {day['recommended_music']}")
        print(f"  格言: {day['wise_quote']}")

def show_api_capabilities():
    """API機能の概要"""
    print("\n\n=== API機能概要 ===")
    
    capabilities = {
        "📊 データ範囲": "2025年全365日",
        "📁 提供形式": "JSON, CSV, XML, TXT",
        "🌐 アクセス": "GitHub Pages (CORS対応)",
        "📱 用途": "占いアプリ、ウェルネスアプリ、ライフスタイルアプリ",
        "💰 料金": "完全無料",
        "🔄 更新": "静的データ (高速レスポンス)"
    }
    
    for key, value in capabilities.items():
        print(f"{key}: {value}")
    
    print("\n🎯 対象ユーザー:")
    users = [
        "アプリ開発者", "Web開発者", "データサイエンティスト",
        "占い関連サービス", "ウェルネス業界", "ライフスタイルメディア"
    ]
    for user in users:
        print(f"  • {user}")

if __name__ == "__main__":
    show_comprehensive_data()
    show_random_samples()
    show_api_capabilities()