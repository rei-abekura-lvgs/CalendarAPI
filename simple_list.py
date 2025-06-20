#!/usr/bin/env python3
import json
from pathlib import Path

def show_data_overview():
    """全データの概要を表示"""
    print("=== 日本暦API データ概要 ===\n")
    
    # 年間データの確認
    all_json = Path("api/2025/all.json")
    if all_json.exists():
        with open(all_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_days = sum(len(month['days']) for month in data['months'])
        
        print(f"📅 対象年: {data['year']}")
        print(f"📊 総日数: {total_days}日")
        print(f"📁 月数: {len(data['months'])}ヶ月")
        print(f"🔄 最終更新: {data['generated_at']}")
        print()
        
        # 各月の日数を表示
        print("📋 月別日数:")
        for month_data in data['months']:
            month_name = month_data['month_name_jp']
            days_count = len(month_data['days'])
            print(f"  {month_name}: {days_count}日")
        print()
        
        # 祝日の確認
        holidays = []
        for month_data in data['months']:
            for day in month_data['days']:
                if day['is_holiday']:
                    holidays.append(f"{day['date']} - {day['holiday_name']}")
        
        print(f"🎌 祝日数: {len(holidays)}日")
        for holiday in holidays:
            print(f"  {holiday}")
        print()
        
        # ファイル一覧
        api_dir = Path("api/2025")
        files = list(api_dir.glob("*"))
        json_files = [f for f in files if f.suffix == '.json']
        csv_files = [f for f in files if f.suffix == '.csv']
        xml_files = [f for f in files if f.suffix == '.xml'] 
        txt_files = [f for f in files if f.suffix == '.txt']
        
        print(f"📁 生成ファイル数: {len(files)}個")
        print(f"  JSON: {len(json_files)}個")
        print(f"  CSV: {len(csv_files)}個") 
        print(f"  XML: {len(xml_files)}個")
        print(f"  TXT: {len(txt_files)}個")
        print()
        
        # 今日のデータサンプル
        import datetime
        today = datetime.date.today()
        current_month = today.month
        current_day = today.day
        
        for month_data in data['months']:
            if month_data['month'] == current_month:
                for day in month_data['days']:
                    if day['day'] == current_day:
                        print(f"🌟 今日({day['date']})のデータ:")
                        print(f"  曜日: {day['weekday']}")
                        print(f"  六曜: {day['rokuyo']}")
                        print(f"  キーワード: {day['daily_keyword']}")
                        print(f"  色: {day['color_of_the_day']}")
                        print(f"  お茶: {day['recommended_tea']}")
                        break
                break
        
    else:
        print("エラー: データファイルが見つかりません")

if __name__ == "__main__":
    show_data_overview()