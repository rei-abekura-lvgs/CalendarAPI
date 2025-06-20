#!/usr/bin/env python3
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import datetime

def generate_all_formats():
    """JSONデータを元に、CSV、XML、TXT形式のファイルを生成"""
    print("追加形式のファイルを生成します...")
    
    api_dir = Path("api/2025")
    
    # 各月のJSONファイルを処理
    for month in range(1, 13):
        json_file = api_dir / f"{month:02d}.json"
        
        if not json_file.exists():
            print(f"警告: {json_file} が見つかりません")
            continue
            
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # CSV形式
        csv_file = api_dir / f"{month:02d}.csv"
        generate_csv(data, csv_file)
        
        # XML形式
        xml_file = api_dir / f"{month:02d}.xml"
        generate_xml(data, xml_file)
        
        # TXT形式（読みやすい形式）
        txt_file = api_dir / f"{month:02d}.txt"
        generate_txt(data, txt_file)
        
        print(f"-> {month}月のファイル生成完了")

def generate_csv(data, output_file):
    """CSV形式でデータを出力"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダー行
        writer.writerow([
            'date', 'weekday', 'weekday_en', 'is_weekend', 'is_holiday', 
            'holiday_name', 'rokuyo', 'daily_keyword', 'color_of_the_day', 
            'recommended_tea'
        ])
        
        # データ行
        for day in data['days']:
            writer.writerow([
                day['date'],
                day['weekday'],
                day['weekday_en'],
                day['is_weekend'],
                day['is_holiday'],
                day['holiday_name'] or '',
                day['rokuyo'],
                day['daily_keyword'],
                day['color_of_the_day'],
                day['recommended_tea']
            ])

def generate_xml(data, output_file):
    """XML形式でデータを出力"""
    root = ET.Element('calendar')
    root.set('year', str(data['year']))
    root.set('month', str(data['month']))
    root.set('month_name_jp', data['month_name_jp'])
    root.set('api_version', data['api_version'])
    root.set('generated_at', data['generated_at'])
    
    for day_data in data['days']:
        day_elem = ET.SubElement(root, 'day')
        for key, value in day_data.items():
            if value is not None:
                day_elem.set(key, str(value))
            else:
                day_elem.set(key, '')
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def generate_txt(data, output_file):
    """TXT形式（人間が読みやすい形式）でデータを出力"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== {data['month_name_jp']} ({data['year']}年) ===\n")
        f.write(f"データ生成: {data['generated_at']}\n")
        f.write(f"APIバージョン: {data['api_version']}\n")
        f.write("-" * 60 + "\n\n")
        
        for day_data in data['days']:
            holiday_mark = "🎌" if day_data['is_holiday'] else "  "
            weekend_mark = "🌸" if day_data['is_weekend'] else "  "
            
            f.write(f"{day_data['date']} ({day_data['weekday']}) {holiday_mark}{weekend_mark}\n")
            
            if day_data['holiday_name']:
                f.write(f"  祝日: {day_data['holiday_name']}\n")
            
            f.write(f"  六曜: {day_data['rokuyo']}\n")
            f.write(f"  今日のキーワード: {day_data['daily_keyword']}\n")
            f.write(f"  今日の色: {day_data['color_of_the_day']}\n")
            f.write(f"  おすすめのお茶: {day_data['recommended_tea']}\n")
            f.write("\n")

def generate_all_data_formats():
    """年間データも各形式で生成"""
    all_json = Path("api/2025/all.json")
    
    if not all_json.exists():
        print("警告: all.json が見つかりません")
        return
        
    with open(all_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 年間データCSV
    csv_file = Path("api/2025/all.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'date', 'weekday', 'weekday_en', 'is_weekend', 'is_holiday', 
            'holiday_name', 'rokuyo', 'daily_keyword', 'color_of_the_day', 
            'recommended_tea'
        ])
        
        for month_data in data['months']:
            for day in month_data['days']:
                writer.writerow([
                    day['date'], day['weekday'], day['weekday_en'],
                    day['is_weekend'], day['is_holiday'], day['holiday_name'] or '',
                    day['rokuyo'], day['daily_keyword'], day['color_of_the_day'],
                    day['recommended_tea']
                ])
    
    print("-> 年間データ (all.csv) 生成完了")

if __name__ == "__main__":
    generate_all_formats()
    generate_all_data_formats()
    print("\n全形式のファイル生成が完了しました！")
    print("利用可能な形式: JSON, CSV, XML, TXT")