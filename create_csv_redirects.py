"""
古いCSVファイル名から新しいファイル名へのシンボリックリンク作成
後方互換性のためのリダイレクト機能
"""

import os
from pathlib import Path

def create_csv_redirects():
    """古いCSVファイル名から新しいファイル名へのシンボリックリンク作成"""
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年のリダイレクト作成中...')
        
        # 月別ファイルのリダイレクト
        for month in range(1, 13):
            # CSVファイル
            old_csv_name = f'{month:02d}.csv'
            new_csv_name = f'{year}-{month:02d}.csv'
            old_csv_path = year_dir / old_csv_name
            new_csv_path = year_dir / new_csv_name
            
            if new_csv_path.exists() and not old_csv_path.exists():
                try:
                    # 相対パスでシンボリックリンク作成
                    os.symlink(new_csv_name, str(old_csv_path))
                    print(f'  ✓ {old_csv_name} → {new_csv_name}')
                except OSError as e:
                    # Windowsの場合はファイルコピーで代替
                    import shutil
                    shutil.copy2(str(new_csv_path), str(old_csv_path))
                    print(f'  ✓ {old_csv_name} → {new_csv_name} (copy)')
            
            # XMLファイル
            old_xml_name = f'{month:02d}.xml'
            new_xml_name = f'{year}-{month:02d}.xml'
            old_xml_path = year_dir / old_xml_name
            new_xml_path = year_dir / new_xml_name
            
            if new_xml_path.exists() and not old_xml_path.exists():
                try:
                    os.symlink(new_xml_name, str(old_xml_path))
                    print(f'  ✓ {old_xml_name} → {new_xml_name}')
                except OSError:
                    import shutil
                    shutil.copy2(str(new_xml_path), str(old_xml_path))
                    print(f'  ✓ {old_xml_name} → {new_xml_name} (copy)')
            
            # TXTファイル
            old_txt_name = f'{month:02d}.txt'
            new_txt_name = f'{year}-{month:02d}.txt'
            old_txt_path = year_dir / old_txt_name
            new_txt_path = year_dir / new_txt_name
            
            if new_txt_path.exists() and not old_txt_path.exists():
                try:
                    os.symlink(new_txt_name, str(old_txt_path))
                    print(f'  ✓ {old_txt_name} → {new_txt_name}')
                except OSError:
                    import shutil
                    shutil.copy2(str(new_txt_path), str(old_txt_path))
                    print(f'  ✓ {old_txt_name} → {new_txt_name} (copy)')
        
        # 年間ファイルのリダイレクト
        file_types = ['csv', 'xml', 'txt']
        for file_type in file_types:
            old_annual_name = f'all.{file_type}'
            new_annual_name = f'{year}-all.{file_type}'
            old_annual_path = year_dir / old_annual_name
            new_annual_path = year_dir / new_annual_name
            
            if new_annual_path.exists() and not old_annual_path.exists():
                try:
                    os.symlink(new_annual_name, str(old_annual_path))
                    print(f'  ✓ {old_annual_name} → {new_annual_name}')
                except OSError:
                    import shutil
                    shutil.copy2(str(new_annual_path), str(old_annual_path))
                    print(f'  ✓ {old_annual_name} → {new_annual_name} (copy)')

def main():
    """メイン処理"""
    print('=== 後方互換性リダイレクト作成 ===')
    create_csv_redirects()
    
    print('\n✅ リダイレクト作成完了')
    print('古いファイル名でのアクセスも可能になりました')

if __name__ == '__main__':
    main()