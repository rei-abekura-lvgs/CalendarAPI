#!/usr/bin/env python3
"""
正確な年間TXTファイル生成ツール
階層構造のJSONデータに対応
"""

import json
from pathlib import Path
from datetime import datetime

def generate_correct_annual_txt(year):
    """正確な年間TXTファイルを生成"""
    json_file = Path(f"api/{year}/all.json")
    txt_file = Path(f"api/{year}/all.txt")
    
    if not json_file.exists():
        print(f"警告: {json_file} が見つかりません")
        return False
        
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 祝日を月別に整理
    holidays_by_month = {}
    total_holidays = 0
    total_days = 0
    
    # データ構造を判定
    if 'months' in data and isinstance(data['months'], list):
        # 階層構造（2026年以降）
        for month_data in data['months']:
            month_num = month_data['month']
            holidays_by_month[month_num] = []
            
            if 'days' in month_data:
                for day_data in month_data['days']:
                    total_days += 1
                    if day_data.get('is_holiday') and day_data.get('holiday_name'):
                        day_num = day_data['day']
                        holiday_name = day_data['holiday_name']
                        holidays_by_month[month_num].append(f"{day_num}日({holiday_name})")
                        total_holidays += 1
    else:
        # フラット構造（2025年）
        for date_str, day_data in data.items():
            if isinstance(date_str, str) and date_str.startswith(str(year)) and '-' in date_str:
                total_days += 1
                if day_data.get('is_holiday') and day_data.get('holiday_name'):
                    month = int(date_str.split('-')[1])
                    day = int(date_str.split('-')[2])
                    holiday_name = day_data.get('holiday_name')
                    
                    if month not in holidays_by_month:
                        holidays_by_month[month] = []
                    holidays_by_month[month].append(f"{day}日({holiday_name})")
                    total_holidays += 1
    
    # TXTファイルに書き込み
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"=== {year}年 年間暦データ ===\n")
        f.write(f"データ生成: {datetime.now().isoformat()}\n")
        f.write("APIバージョン: v1\n")
        f.write("-" * 60 + "\n\n")
        
        # 月別祝日一覧
        for month in range(1, 13):
            f.write(f"【{month}月】\n")
            if month in holidays_by_month and holidays_by_month[month]:
                f.write(f"  祝日: {', '.join(holidays_by_month[month])}\n")
            else:
                f.write("  祝日: なし\n")
            f.write("\n")
        
        f.write(f"年間祝日総数: {total_holidays}日\n")
        f.write(f"総日数: {total_days}日\n\n")
        f.write("※ 詳細データは対応するJSONまたはCSVファイルをご参照ください。\n")
    
    print(f"✓ {txt_file} を修正しました（{total_holidays}日の祝日、{total_days}日総数）")
    return True

def main():
    """全年のTXTファイルを修正"""
    print("年間TXTファイル修正ツール")
    print("=" * 40)
    
    years = range(2025, 2037)  # 2025-2036年
    
    for year in years:
        print(f"\n{year}年のTXTファイルを修正中...")
        generate_correct_annual_txt(year)
    
    print(f"\n全年間TXTファイル修正完了")

if __name__ == "__main__":
    main()