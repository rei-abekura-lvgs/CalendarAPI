"""
日本語ファイル名をURL対応英語ファイル名に変更
"""

import os
from pathlib import Path

def rename_files_to_url_safe():
    """日本語ファイル名をURL対応名に変更"""
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年のファイル名修正中...')
        
        # 月別ファイルのリネーム
        for month in range(1, 13):
            # CSVファイル
            japanese_csv = year_dir / f'{year}年{month:02d}月.csv'
            english_csv = year_dir / f'{year}-{month:02d}.csv'
            
            if japanese_csv.exists():
                japanese_csv.rename(english_csv)
                print(f'  ✓ {japanese_csv.name} → {english_csv.name}')
            
            # XMLファイル
            japanese_xml = year_dir / f'{year}年{month:02d}月.xml'
            english_xml = year_dir / f'{year}-{month:02d}.xml'
            
            if japanese_xml.exists():
                japanese_xml.rename(english_xml)
                print(f'  ✓ {japanese_xml.name} → {english_xml.name}')
            
            # TXTファイル
            japanese_txt = year_dir / f'{year}年{month:02d}月.txt'
            english_txt = year_dir / f'{year}-{month:02d}.txt'
            
            if japanese_txt.exists():
                japanese_txt.rename(english_txt)
                print(f'  ✓ {japanese_txt.name} → {english_txt.name}')
        
        # 年間ファイルのリネーム
        file_types = ['csv', 'xml', 'txt']
        for file_type in file_types:
            japanese_annual = year_dir / f'{year}年全年.{file_type}'
            english_annual = year_dir / f'{year}-all.{file_type}'
            
            if japanese_annual.exists():
                japanese_annual.rename(english_annual)
                print(f'  ✓ {japanese_annual.name} → {english_annual.name}')

def main():
    """メイン処理"""
    print('=== ファイル名URL対応修正 ===')
    rename_files_to_url_safe()
    
    print('\n✅ ファイル名修正完了')
    print('新しいファイル名形式:')
    print('・月別: 2026-01.csv, 2026-02.xml, 2026-03.txt')
    print('・年間: 2026-all.csv, 2026-all.xml, 2026-all.txt')

if __name__ == '__main__':
    main()