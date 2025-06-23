"""
欠落しているXML・TXTファイルを新ファイル名形式で生成
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

def generate_xml_from_json(json_path, xml_path):
    """JSONファイルからXMLファイルを生成"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # XMLルート要素作成
    if isinstance(data, dict) and 'months' in data:
        # 年間データの場合
        root = ET.Element('calendar_data')
        root.set('year', str(data['year']))
        root.set('api_version', data['api_version'])
        
        for month_data in data['months']:
            month_elem = ET.SubElement(root, 'month')
            month_elem.set('number', str(month_data['month']))
            month_elem.set('name', month_data['month_name_jp'])
            
            for day_data in month_data['days']:
                day_elem = ET.SubElement(month_elem, 'day')
                for key, value in day_data.items():
                    if isinstance(value, bool):
                        day_elem.set(key, str(value).lower())
                    elif value is not None:
                        day_elem.set(key, str(value))
    else:
        # 月別データの場合
        root = ET.Element('month_data')
        if isinstance(data, dict):
            root.set('year', str(data.get('year', '')))
            root.set('month', str(data.get('month', '')))
            root.set('month_name', data.get('month_name_jp', ''))
            
            if 'days' in data:
                for day_data in data['days']:
                    day_elem = ET.SubElement(root, 'day')
                    for key, value in day_data.items():
                        if isinstance(value, bool):
                            day_elem.set(key, str(value).lower())
                        elif value is not None:
                            day_elem.set(key, str(value))
    
    # XMLファイル保存
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

def generate_txt_from_json(json_path, txt_path):
    """JSONファイルからTXTファイルを生成"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = []
    
    if isinstance(data, dict) and 'months' in data:
        # 年間データの場合
        year = data['year']
        content.append(f"{year}年 暦データ")
        content.append("=" * 40)
        content.append("")
        
        # 祝日一覧
        holidays = []
        total_days = 0
        ichiryu_days = 0
        kuubou_days = 0
        
        for month_data in data['months']:
            for day_data in month_data['days']:
                total_days += 1
                if day_data.get('is_holiday'):
                    holidays.append(f"{day_data['date']} ({day_data['weekday']}) - {day_data.get('holiday_name', '')}")
                if day_data.get('is_ichiryu_manbai'):
                    ichiryu_days += 1
                if day_data.get('is_kuubou'):
                    kuubou_days += 1
        
        content.append(f"総日数: {total_days}日")
        content.append(f"祝日数: {len(holidays)}日")
        content.append(f"一粒万倍日: {ichiryu_days}日")
        content.append(f"空亡日: {kuubou_days}日")
        content.append("")
        
        content.append("祝日一覧:")
        content.append("-" * 20)
        if holidays:
            content.extend(holidays)
        else:
            content.append("祝日なし")
        
    else:
        # 月別データの場合
        if isinstance(data, dict):
            year = data.get('year', '')
            month = data.get('month', '')
            month_name = data.get('month_name_jp', '')
            
            content.append(f"{year}年{month}月({month_name}) 暦データ")
            content.append("=" * 40)
            content.append("")
            
            if 'days' in data:
                holidays = []
                ichiryu_days = []
                kuubou_days = []
                
                for day_data in data['days']:
                    if day_data.get('is_holiday'):
                        holidays.append(f"{day_data['date']} - {day_data.get('holiday_name', '')}")
                    if day_data.get('is_ichiryu_manbai'):
                        ichiryu_days.append(day_data['date'])
                    if day_data.get('is_kuubou'):
                        kuubou_days.append(day_data['date'])
                
                content.append(f"総日数: {len(data['days'])}日")
                content.append(f"祝日数: {len(holidays)}日")
                content.append(f"一粒万倍日: {len(ichiryu_days)}日")
                content.append(f"空亡日: {len(kuubou_days)}日")
                content.append("")
                
                if holidays:
                    content.append("祝日:")
                    content.extend(holidays)
                    content.append("")
                
                if ichiryu_days:
                    content.append("一粒万倍日:")
                    content.extend(ichiryu_days)
                    content.append("")
                
                if kuubou_days:
                    content.append("空亡日:")
                    content.extend(kuubou_days)
    
    # TXTファイル保存
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def generate_missing_files():
    """欠落しているファイルを生成"""
    
    generated_count = 0
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年の欠落ファイル生成中...')
        
        # 月別ファイル生成
        for month in range(1, 13):
            json_file = year_dir / f'{month:02d}.json'
            xml_file = year_dir / f'{year}-{month:02d}.xml'
            txt_file = year_dir / f'{year}-{month:02d}.txt'
            
            if json_file.exists():
                # XMLファイル生成
                if not xml_file.exists():
                    try:
                        generate_xml_from_json(json_file, xml_file)
                        generated_count += 1
                        print(f'  ✓ 生成: {xml_file.name}')
                    except Exception as e:
                        print(f'  ✗ エラー: {xml_file.name} - {e}')
                
                # TXTファイル生成
                if not txt_file.exists():
                    try:
                        generate_txt_from_json(json_file, txt_file)
                        generated_count += 1
                        print(f'  ✓ 生成: {txt_file.name}')
                    except Exception as e:
                        print(f'  ✗ エラー: {txt_file.name} - {e}')
        
        # 年間ファイル生成
        annual_json = year_dir / 'all.json'
        annual_xml = year_dir / f'{year}-all.xml'
        annual_txt = year_dir / f'{year}-all.txt'
        
        if annual_json.exists():
            # 年間XMLファイル生成
            if not annual_xml.exists():
                try:
                    generate_xml_from_json(annual_json, annual_xml)
                    generated_count += 1
                    print(f'  ✓ 生成: {annual_xml.name}')
                except Exception as e:
                    print(f'  ✗ エラー: {annual_xml.name} - {e}')
            
            # 年間TXTファイル（既存のものがあれば上書き）
            try:
                generate_txt_from_json(annual_json, annual_txt)
                generated_count += 1
                print(f'  ✓ 生成: {annual_txt.name}')
            except Exception as e:
                print(f'  ✗ エラー: {annual_txt.name} - {e}')
    
    return generated_count

def main():
    """メイン処理"""
    print('=== 欠落ファイル生成（新ファイル名形式） ===')
    
    generated_count = generate_missing_files()
    
    print(f'\n✅ 生成完了: {generated_count}個のファイル')
    print('新ファイル名形式で統一されました')

if __name__ == '__main__':
    main()