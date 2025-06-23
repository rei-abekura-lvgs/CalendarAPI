"""
CSV文字化け修正とファイル名改善、年間TXT内容追加ツール
"""

import json
import csv
import os
from pathlib import Path

def fix_csv_encoding_and_rename():
    """CSV文字化け修正とファイル名を分かりやすく変更"""
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年のファイル修正中...')
        
        # 月別CSVファイルの修正とリネーム
        for month in range(1, 13):
            old_csv = year_dir / f'{month:02d}.csv'
            new_csv = year_dir / f'{year}年{month:02d}月.csv'
            
            if old_csv.exists():
                # CSVファイルを正しいUTF-8で再保存（BOM無し）
                with open(old_csv, 'r', encoding='utf-8-sig') as f:
                    content = f.read()
                
                # BOM無しUTF-8で保存
                with open(new_csv, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                
                # 古いファイルを削除
                old_csv.unlink()
                print(f'  ✓ {old_csv.name} → {new_csv.name}')
        
        # 年間CSVファイルの修正とリネーム
        old_annual_csv = year_dir / 'all.csv'
        new_annual_csv = year_dir / f'{year}年全年.csv'
        
        if old_annual_csv.exists():
            with open(old_annual_csv, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            with open(new_annual_csv, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            
            old_annual_csv.unlink()
            print(f'  ✓ {old_annual_csv.name} → {new_annual_csv.name}')

def generate_annual_txt_content():
    """年間TXTファイルに実際の祝日データを追加"""
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年の年間TXT生成中...')
        
        # 年間JSONデータを読み込み
        annual_json = year_dir / 'all.json'
        if not annual_json.exists():
            continue
            
        with open(annual_json, 'r', encoding='utf-8') as f:
            year_data = json.load(f)
        
        # 祝日を抽出（正しいJSON構造に対応）
        holidays = []
        total_days = 0
        ichiryu_days = 0
        kuubou_days = 0
        
        # year_data['months']のリストから各月のdaysを処理
        for month_data in year_data.get('months', []):
            for day_data in month_data.get('days', []):
                total_days += 1
                
                if day_data.get('is_holiday'):
                    holidays.append({
                        'date': day_data['date'],
                        'name': day_data.get('holiday_name', ''),
                        'weekday': day_data['weekday']
                    })
                
                if day_data.get('is_ichiryu_manbai'):
                    ichiryu_days += 1
                
                if day_data.get('is_kuubou'):
                    kuubou_days += 1
        
        # TXTファイル作成
        txt_content = f"""{year}年 暦データ統計
========================================

■ 基本情報
総日数: {total_days}日
祝日数: {len(holidays)}日
一粒万倍日: {ichiryu_days}日
空亡日: {kuubou_days}日

■ 祝日一覧
"""
        
        if holidays:
            for holiday in holidays:
                txt_content += f"{holiday['date']} ({holiday['weekday']}) - {holiday['name']}\n"
        else:
            txt_content += "祝日データなし\n"
        
        txt_content += f"""
■ 特殊日統計
・一粒万倍日: 年間{ichiryu_days}回
・空亡日: 年間{kuubou_days}回

■ データ項目
39の詳細項目を提供：
基本情報、祝日、六曜、一粒万倍日、十干十二支、
五行、陰陽、動物、十二運、空亡、二十四節気、
月相、キーワード、色、推奨茶、ラッキーナンバー、
パワーストーン、アロマオイル、瞑想テーマ、
花言葉、エネルギーアドバイス、占星術、タロット、
名言、音楽推奨、食事推奨、クリスタルヒーリング、風水

本データは暦データAPIにより生成されました。
"""
        
        # ファイル保存
        txt_file = year_dir / f'{year}年全年.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        # 古いall.txtがあれば削除
        old_txt = year_dir / 'all.txt'
        if old_txt.exists():
            old_txt.unlink()
        
        print(f'  ✓ {txt_file.name} 生成完了（祝日{len(holidays)}件）')

def main():
    """メイン処理"""
    print('=== CSV文字化け修正とファイル名改善 ===')
    fix_csv_encoding_and_rename()
    
    print('\n=== 年間TXTファイル内容生成 ===')
    generate_annual_txt_content()
    
    print('\n✅ 全修正完了')
    print('・CSV文字化け修正（BOM削除）')
    print('・ファイル名をわかりやすく変更')
    print('・年間TXTに実際の祝日データ追加')

if __name__ == '__main__':
    main()