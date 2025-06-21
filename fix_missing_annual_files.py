#!/usr/bin/env python3
"""
欠落している年間データファイル（CSV、XML、TXT）を生成
2026年〜2036年の年間データファイルを完全生成
"""

import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

def generate_annual_csv(year):
    """年間データのCSV形式を生成"""
    json_file = Path(f"api/{year}/all.json")
    csv_file = Path(f"api/{year}/all.csv")
    
    if not json_file.exists():
        print(f"警告: {json_file} が見つかりません")
        return False
        
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CSVヘッダーを定義（27項目対応）
    headers = [
        'date', 'year', 'month', 'day', 'weekday', 'weekday_en',
        'is_holiday', 'holiday_name', 'is_weekend', 'rokuyo',
        'daily_keyword', 'color_of_the_day', 'recommended_tea',
        'lucky_number', 'power_stone', 'aroma_oil', 'meditation_theme',
        'flower_language', 'energy_advice', 'astrology_advice',
        'tarot_card', 'wise_saying', 'recommended_music',
        'recommended_food', 'crystal_healing', 'feng_shui_advice',
        'daily_affirmation'
    ]
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # 各日のデータを書き込み
        for date_str, day_data in data.items():
            if date_str.startswith(str(year)):  # 年でフィルタ
                row = [
                    day_data.get('date', ''),
                    day_data.get('year', ''),
                    day_data.get('month', ''),
                    day_data.get('day', ''),
                    day_data.get('weekday', ''),
                    day_data.get('weekday_en', ''),
                    day_data.get('is_holiday', False),
                    day_data.get('holiday_name', ''),
                    day_data.get('is_weekend', False),
                    day_data.get('rokuyo', ''),
                    day_data.get('daily_keyword', ''),
                    day_data.get('color_of_the_day', ''),
                    day_data.get('recommended_tea', ''),
                    day_data.get('lucky_number', ''),
                    day_data.get('power_stone', ''),
                    day_data.get('aroma_oil', ''),
                    day_data.get('meditation_theme', ''),
                    day_data.get('flower_language', ''),
                    day_data.get('energy_advice', ''),
                    day_data.get('astrology_advice', ''),
                    day_data.get('tarot_card', ''),
                    day_data.get('wise_saying', ''),
                    day_data.get('recommended_music', ''),
                    day_data.get('recommended_food', ''),
                    day_data.get('crystal_healing', ''),
                    day_data.get('feng_shui_advice', ''),
                    day_data.get('daily_affirmation', '')
                ]
                writer.writerow(row)
    
    print(f"✓ {csv_file} を生成しました")
    return True

def generate_annual_xml(year):
    """年間データのXML形式を生成"""
    json_file = Path(f"api/{year}/all.json")
    xml_file = Path(f"api/{year}/all.xml")
    
    if not json_file.exists():
        print(f"警告: {json_file} が見つかりません")
        return False
        
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # XMLルート要素を作成
    root = ET.Element('calendar')
    root.set('year', str(year))
    root.set('generated_at', datetime.now().isoformat())
    root.set('api_version', 'v1')
    
    # 各日のデータを追加
    for date_str, day_data in data.items():
        if date_str.startswith(str(year)):  # 年でフィルタ
            day_elem = ET.SubElement(root, 'day')
            day_elem.set('date', date_str)
            
            # 27項目すべてを追加
            for key, value in day_data.items():
                elem = ET.SubElement(day_elem, key)
                if value is not None:
                    elem.text = str(value)
                else:
                    elem.text = ''
    
    # XMLファイルに書き込み
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    
    print(f"✓ {xml_file} を生成しました")
    return True

def generate_annual_txt(year):
    """年間データのTXT形式を生成（祝日概要）"""
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
    
    for date_str, day_data in data.items():
        if date_str.startswith(str(year)):
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
            if month in holidays_by_month:
                f.write(f"  祝日: {', '.join(holidays_by_month[month])}\n")
            else:
                f.write("  祝日: なし\n")
            f.write("\n")
        
        f.write(f"年間祝日総数: {total_holidays}日\n")
        f.write(f"総日数: {total_days}日\n\n")
        f.write("※ 詳細データは対応するJSONまたはCSVファイルをご参照ください。\n")
    
    print(f"✓ {txt_file} を生成しました")
    return True

def main():
    """メイン処理：欠落しているファイルを生成"""
    print("欠落している年間データファイル生成ツール")
    print("=" * 50)
    
    years = range(2026, 2037)  # 2026-2036年
    
    for year in years:
        print(f"\n{year}年のファイルを生成中...")
        
        success_count = 0
        if generate_annual_csv(year):
            success_count += 1
        if generate_annual_xml(year):
            success_count += 1
        if generate_annual_txt(year):
            success_count += 1
        
        print(f"{year}年: {success_count}/3 ファイル生成完了")
    
    print(f"\n全年間データファイル生成完了")
    print("生成されたファイル:")
    print("- CSV: 年間データ（27項目完全対応）")
    print("- XML: 年間データ（構造化）")
    print("- TXT: 年間祝日概要（人間可読）")

if __name__ == "__main__":
    main()