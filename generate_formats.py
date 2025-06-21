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
            'recommended_tea', 'lucky_number', 'power_stone', 'aroma_oil',
            'meditation_theme', 'flower_of_the_day', 'energy_advice',
            'zodiac_influence', 'tarot_card', 'wise_quote', 'recommended_music',
            'recommended_food', 'crystal_healing', 'feng_shui_tip'
        ])
        
        for month_data in data['months']:
            for day in month_data['days']:
                writer.writerow([
                    day['date'], day['weekday'], day['weekday_en'],
                    day['is_weekend'], day['is_holiday'], day['holiday_name'] or '',
                    day['rokuyo'], day['daily_keyword'], day['color_of_the_day'],
                    day['recommended_tea'], day['lucky_number'], day['power_stone'],
                    day['aroma_oil'], day['meditation_theme'], day['flower_of_the_day'],
                    day['energy_advice'], day['zodiac_influence'], day['tarot_card'],
                    day['wise_quote'], day['recommended_music'], day['recommended_food'],
                    day['crystal_healing'], day['feng_shui_tip']
                ])
    
    print("-> 年間データ (all.csv) 生成完了")
    
    # 年間データXML
    xml_file = Path("api/2025/all.xml")
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<calendar>\n')
        f.write(f'  <year>{data["year"]}</year>\n')
        f.write(f'  <api_version>{data["api_version"]}</api_version>\n')
        f.write(f'  <generated_at>{data["generated_at"]}</generated_at>\n')
        f.write('  <months>\n')
        
        for month_data in data['months']:
            f.write(f'    <month number="{month_data["month"]}" name="{month_data["month_name"]}">\n')
            f.write('      <days>\n')
            
            for day in month_data['days']:
                f.write(f'        <day number="{day["day"]}">\n')
                f.write(f'          <date>{day["date"]}</date>\n')
                f.write(f'          <weekday>{day["weekday"]}</weekday>\n')
                f.write(f'          <weekday_en>{day["weekday_en"]}</weekday_en>\n')
                f.write(f'          <is_weekend>{str(day["is_weekend"]).lower()}</is_weekend>\n')
                f.write(f'          <is_holiday>{str(day["is_holiday"]).lower()}</is_holiday>\n')
                if day["holiday_name"]:
                    f.write(f'          <holiday_name>{day["holiday_name"]}</holiday_name>\n')
                f.write(f'          <rokuyo>{day["rokuyo"]}</rokuyo>\n')
                f.write(f'          <daily_keyword>{day["daily_keyword"]}</daily_keyword>\n')
                f.write(f'          <color_of_the_day>{day["color_of_the_day"]}</color_of_the_day>\n')
                f.write(f'          <recommended_tea>{day["recommended_tea"]}</recommended_tea>\n')
                f.write(f'          <lucky_number>{day["lucky_number"]}</lucky_number>\n')
                f.write(f'          <power_stone>{day["power_stone"]}</power_stone>\n')
                f.write(f'          <aroma_oil>{day["aroma_oil"]}</aroma_oil>\n')
                f.write(f'          <meditation_theme>{day["meditation_theme"]}</meditation_theme>\n')
                f.write(f'          <flower_of_the_day>{day["flower_of_the_day"]}</flower_of_the_day>\n')
                f.write(f'          <energy_advice>{day["energy_advice"]}</energy_advice>\n')
                f.write(f'          <zodiac_influence>{day["zodiac_influence"]}</zodiac_influence>\n')
                f.write(f'          <tarot_card>{day["tarot_card"]}</tarot_card>\n')
                f.write(f'          <wise_quote>{day["wise_quote"]}</wise_quote>\n')
                f.write(f'          <recommended_music>{day["recommended_music"]}</recommended_music>\n')
                f.write(f'          <recommended_food>{day["recommended_food"]}</recommended_food>\n')
                f.write(f'          <crystal_healing>{day["crystal_healing"]}</crystal_healing>\n')
                f.write(f'          <feng_shui_tip>{day["feng_shui_tip"]}</feng_shui_tip>\n')
                f.write('        </day>\n')
            
            f.write('      </days>\n')
            f.write('    </month>\n')
        
        f.write('  </months>\n')
        f.write('</calendar>\n')
    
    print("-> 年間データ (all.xml) 生成完了")
    
    # 年間データTXT（要約版）
    txt_file = Path("api/2025/all.txt")
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"=== {data['year']}年 年間暦データ ===\n")
        f.write(f"データ生成: {data['generated_at']}\n")
        f.write(f"APIバージョン: {data['api_version']}\n")
        f.write("-" * 60 + "\n\n")
        
        total_holidays = 0
        for month_data in data['months']:
            f.write(f"【{month_data['month_name_jp']}】\n")
            holidays_in_month = [day for day in month_data['days'] if day['is_holiday']]
            if holidays_in_month:
                f.write("  祝日: ")
                f.write(", ".join([f"{day['day']}日({day['holiday_name']})" for day in holidays_in_month]))
                f.write("\n")
                total_holidays += len(holidays_in_month)
            else:
                f.write("  祝日: なし\n")
            f.write("\n")
        
        f.write(f"年間祝日総数: {total_holidays}日\n")
        f.write(f"総日数: {sum(len(month['days']) for month in data['months'])}日\n")
        f.write("\n※ 詳細データは対応するJSONまたはCSVファイルをご参照ください。\n")
    
    print("-> 年間データ (all.txt) 生成完了")

if __name__ == "__main__":
    generate_all_formats()
    generate_all_data_formats()
    print("\n全形式のファイル生成が完了しました！")
    print("利用可能な形式: JSON, CSV, XML, TXT")