#!/usr/bin/env python3
import json
import sys
from datetime import datetime

def display_month_data(month=None):
    """指定された月のデータを表示する"""
    if month is None:
        # 現在の月を取得
        month = datetime.now().month
    
    try:
        with open(f'api/2025/{month:02d}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n=== {data['month_name_jp']} ({data['year']}年) ===")
        print(f"データ生成日時: {data['generated_at']}")
        print(f"API バージョン: {data['api_version']}")
        print("-" * 80)
        
        for day_data in data['days']:
            # 祝日マーク
            holiday_mark = "🎌" if day_data['is_holiday'] else "  "
            weekend_mark = "🌸" if day_data['is_weekend'] else "  "
            
            print(f"{day_data['date']} ({day_data['weekday']}) {holiday_mark}{weekend_mark}")
            if day_data['holiday_name']:
                print(f"    祝日: {day_data['holiday_name']}")
            print(f"    六曜: {day_data['rokuyo']}")
            print(f"    今日のキーワード: {day_data['daily_keyword']}")
            print(f"    今日の色: {day_data['color_of_the_day']}")
            print(f"    おすすめのお茶: {day_data['recommended_tea']}")
            print()
            
    except FileNotFoundError:
        print(f"エラー: {month}月のデータファイルが見つかりません")
    except json.JSONDecodeError:
        print(f"エラー: {month}月のデータファイルが破損しています")

if __name__ == "__main__":
    # コマンドライン引数で月を指定可能
    if len(sys.argv) > 1:
        try:
            month = int(sys.argv[1])
            if 1 <= month <= 12:
                display_month_data(month)
            else:
                print("月は1-12の範囲で指定してください")
        except ValueError:
            print("月は数値で指定してください")
    else:
        # 引数がない場合は現在の月を表示
        display_month_data()