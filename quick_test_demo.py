#!/usr/bin/env python3
"""
暦データAPI クイックテスト & デモンストレーション

Replitでの実用的なテスト方法を実演します。
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def demo_browser_testing():
    """ブラウザでのテスト方法デモ"""
    print("🌐 ブラウザテスト方法:")
    print("1. メインページ: http://localhost:5000")
    print("2. 全ファイル一覧: http://localhost:5000/api_index.html")
    print("3. 今日のデータ: http://localhost:5000/api/2025/06.json")
    print("4. クイックアクセスでリンクをクリック")
    print()

def demo_curl_testing():
    """cURLでのテスト方法デモ"""
    print("🔧 cURLコマンドテスト:")
    print("# 基本テスト")
    print("curl http://localhost:5000/api/2025/06.json")
    print()
    print("# きれいに整形して表示")
    print("curl -s http://localhost:5000/api/2025/06.json | python -m json.tool")
    print()
    print("# ファイルサイズ確認")
    print("curl -I http://localhost:5000/api/2025/all.xml")
    print()
    print("# CSVファイルダウンロード")
    print("curl -o calendar.csv http://localhost:5000/api/2025/01.csv")
    print()

def demo_quick_data_check():
    """データ内容の即座確認"""
    print("📊 データ内容確認:")
    
    try:
        # 今日のデータをチェック
        today = datetime.now()
        month = f"{today.month:02d}"
        
        response = requests.get(f"{BASE_URL}/api/2025/{month}.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            today_data = next((d for d in data['days'] if d['day'] == today.day), None)
            
            if today_data:
                print(f"✅ 今日({today.month}/{today.day})のデータ:")
                print(f"   曜日: {today_data['weekday']}")
                print(f"   六曜: {today_data['rokuyo']}")
                print(f"   キーワード: {today_data['daily_keyword']}")
                print(f"   ラッキーナンバー: {today_data['lucky_number']}")
                print(f"   パワーストーン: {today_data['power_stone']}")
                print()
        
        # ファイル形式確認
        formats = ['json', 'csv', 'xml', 'txt']
        print("📋 利用可能形式:")
        for fmt in formats:
            url = f"{BASE_URL}/api/2025/01.{fmt}"
            try:
                resp = requests.head(url, timeout=3)
                size = int(resp.headers.get('content-length', 0))
                print(f"   {fmt.upper()}: ✅ ({size:,} bytes)")
            except:
                print(f"   {fmt.upper()}: ❌")
        print()
        
    except Exception as e:
        print(f"❌ データ確認エラー: {e}")

def demo_common_issues():
    """よくある問題とその解決法"""
    print("🔧 よくある問題と解決法:")
    print()
    print("【問題1】今日のデータが表示されない")
    print("解決法:")
    print("- ブラウザの開発者ツール（F12）でエラーをチェック")
    print("- ネットワークタブで404エラーを確認")
    print("- python test_api.py でサーバー側テスト")
    print()
    
    print("【問題2】クイックアクセスで404エラー")
    print("解決法:")
    print("- 環境自動判定で修正済み（Replit用URL使用）")
    print("- ブラウザをリロード")
    print()
    
    print("【問題3】文字化け")
    print("解決法:")
    print("- UTF-8エンコーディング確認済み")
    print("- ブラウザの文字エンコーディング設定確認")
    print()

def demo_development_workflow():
    """開発ワークフローのデモ"""
    print("⚙️ 開発ワークフロー:")
    print()
    print("1. データ生成:")
    print("   python generate_data.py")
    print("   python generate_formats.py")
    print()
    print("2. サーバー起動:")
    print("   Replitワークフロー 'Documentation Site' を使用")
    print("   または: python -m http.server 5000")
    print()
    print("3. テスト実行:")
    print("   python test_api.py          # 自動テスト")
    print("   python quick_test_demo.py   # このデモ")
    print()
    print("4. ブラウザ確認:")
    print("   http://localhost:5000")
    print()
    print("5. 問題修正:")
    print("   - コード修正")
    print("   - ワークフロー再起動")
    print("   - 再テスト")
    print()

def demo_api_usage_examples():
    """実用的なAPI使用例"""
    print("💡 実用的なAPI使用例:")
    print()
    
    print("【JavaScript例】")
    print('''
// 今月のイベントを取得
fetch('./api/2025/06.json')
  .then(response => response.json())
  .then(data => {
    const holidays = data.days.filter(day => day.is_holiday);
    console.log('今月の祝日:', holidays);
  });
''')
    print()
    
    print("【Python例】")
    print('''
import requests

# 年間祝日一覧を取得
response = requests.get('http://localhost:5000/api/2025/all.json')
data = response.json()

holidays = []
for month in data['months']:
    for day in month['days']:
        if day['is_holiday']:
            holidays.append({
                'date': day['date'],
                'name': day['holiday_name']
            })

print(f"2025年の祝日: {len(holidays)}日")
for holiday in holidays:
    print(f"  {holiday['date']}: {holiday['name']}")
''')
    print()

def main():
    """メインデモ実行"""
    print("🎯 暦データAPI - 実用テストガイド")
    print("=" * 60)
    print()
    
    demo_browser_testing()
    demo_curl_testing()
    demo_quick_data_check()
    demo_common_issues()
    demo_development_workflow()
    demo_api_usage_examples()
    
    print("🎉 デモ完了!")
    print()
    print("💡 次のステップ:")
    print("1. ブラウザで http://localhost:5000 にアクセス")
    print("2. クイックアクセスで各リンクをテスト")
    print("3. 全ファイル一覧ページで形式を確認")
    print("4. 開発者ツールでネットワーク通信を監視")

if __name__ == "__main__":
    main()