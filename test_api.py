#!/usr/bin/env python3
"""
暦データAPI テストツール

このスクリプトはReplitでAPIの動作確認を行うためのテストツールです。
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, description):
    """エンドポイントをテストする"""
    print(f"\n📡 テスト: {description}")
    print(f"🔗 URL: {BASE_URL}{endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ ステータス: {response.status_code} OK")
            
            # JSONかどうかチェック
            if 'application/json' in response.headers.get('content-type', ''):
                data = response.json()
                print(f"📊 データサイズ: {len(json.dumps(data))} bytes")
                
                # 基本構造をチェック
                if 'days' in data:
                    print(f"📅 日数: {len(data['days'])} 日")
                    if data['days']:
                        first_day = data['days'][0]
                        print(f"🔍 サンプル項目数: {len(first_day)} 項目")
                        print(f"🎯 サンプルキーワード: {first_day.get('daily_keyword', 'N/A')}")
                        
            else:
                print(f"📊 ファイルサイズ: {len(response.content)} bytes")
                
        else:
            print(f"❌ エラー: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 接続エラー: {e}")

def test_today_data():
    """今日のデータを取得テスト"""
    today = datetime.now()
    month = f"{today.month:02d}"
    day = today.day
    
    endpoint = f"/api/2025/{month}.json"
    print(f"\n🗓️  今日のデータテスト ({today.year}-{month}-{day:02d})")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            today_data = next((d for d in data['days'] if d['day'] == day), None)
            
            if today_data:
                print("✅ 今日のデータが見つかりました")
                print(f"📅 日付: {today_data['date']}")
                print(f"🗓️  曜日: {today_data['weekday']}")
                print(f"🎯 キーワード: {today_data['daily_keyword']}")
                print(f"🎨 今日の色: {today_data['color_of_the_day']}")
                print(f"🔢 ラッキーナンバー: {today_data['lucky_number']}")
            else:
                print("❌ 今日のデータが見つかりません")
        else:
            print(f"❌ エラー: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def main():
    """メインテスト関数"""
    print("🧪 暦データAPI テストツール")
    print("=" * 50)
    
    # 基本テスト
    test_endpoint("/", "メインページ")
    test_endpoint("/api_index.html", "全ファイル一覧ページ")
    
    # APIエンドポイントテスト
    test_endpoint("/api/2025/01.json", "1月JSONデータ")
    test_endpoint("/api/2025/06.json", "6月JSONデータ")
    test_endpoint("/api/2025/12.json", "12月JSONデータ")
    
    # 複数形式テスト
    test_endpoint("/api/2025/01.csv", "1月CSVデータ")
    test_endpoint("/api/2025/01.xml", "1月XMLデータ")
    test_endpoint("/api/2025/01.txt", "1月TXTデータ")
    
    # 年間データテスト
    test_endpoint("/api/2025/all.json", "2025年全データ")
    test_endpoint("/api/2025/all.csv", "2025年全データ(CSV)")
    
    # 複数年テスト
    test_endpoint("/api/2026/06.json", "2026年6月データ")
    test_endpoint("/api/2030/12.json", "2030年12月データ")
    
    # 今日のデータテスト
    test_today_data()
    
    print("\n🎉 テスト完了!")
    print("\n💡 使い方:")
    print("  python test_api.py")
    print("  または")
    print("  chmod +x test_api.py && ./test_api.py")

if __name__ == "__main__":
    main()