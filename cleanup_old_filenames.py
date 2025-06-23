"""
古いファイル名を削除して新しいファイル名に統一
ダウンロード時のファイル名も修正
"""

import os
from pathlib import Path

def remove_old_filename_links():
    """古いファイル名のシンボリックリンクを削除"""
    
    removed_count = 0
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年の古いファイル名削除中...')
        
        # 月別ファイルの古いリンク削除
        for month in range(1, 13):
            old_files = [
                f'{month:02d}.csv',
                f'{month:02d}.xml', 
                f'{month:02d}.txt'
            ]
            
            for old_file in old_files:
                old_path = year_dir / old_file
                if old_path.exists():
                    old_path.unlink()
                    removed_count += 1
                    print(f'  ✓ 削除: {old_file}')
        
        # 年間ファイルの古いリンク削除
        old_annual_files = ['all.csv', 'all.xml', 'all.txt']
        for old_file in old_annual_files:
            old_path = year_dir / old_file
            if old_path.exists():
                old_path.unlink()
                removed_count += 1
                print(f'  ✓ 削除: {old_file}')
    
    return removed_count

def create_download_filename_htaccess():
    """ダウンロード時のファイル名を適切に設定する.htaccess作成"""
    
    htaccess_content = """# ダウンロード時のファイル名設定
<FilesMatch "\\.(csv|xml|txt)$">
    Header set Content-Disposition "attachment"
</FilesMatch>

# CSVファイルの正しいMIMEタイプとファイル名
<FilesMatch "\\.csv$">
    Header set Content-Type "text/csv; charset=utf-8"
</FilesMatch>

# XMLファイルの正しいMIMEタイプ
<FilesMatch "\\.xml$">
    Header set Content-Type "application/xml; charset=utf-8"
</FilesMatch>

# TXTファイルの正しいMIMEタイプ
<FilesMatch "\\.txt$">
    Header set Content-Type "text/plain; charset=utf-8"
</FilesMatch>

# キャッシュ設定
<FilesMatch "\\.(json|csv|xml|txt)$">
    Header set Cache-Control "public, max-age=3600"
</FilesMatch>
"""
    
    # 各年のディレクトリに.htaccessを作成
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if year_dir.exists():
            htaccess_path = year_dir / '.htaccess'
            with open(htaccess_path, 'w', encoding='utf-8') as f:
                f.write(htaccess_content)
            print(f'✓ {htaccess_path} 作成完了')

def verify_new_filenames():
    """新しいファイル名の存在確認"""
    
    total_files = 0
    missing_files = []
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        # 月別ファイルチェック
        for month in range(1, 13):
            for ext in ['csv', 'xml', 'txt']:
                new_filename = f'{year}-{month:02d}.{ext}'
                new_path = year_dir / new_filename
                
                if new_path.exists():
                    total_files += 1
                else:
                    missing_files.append(f'{year}/{new_filename}')
        
        # 年間ファイルチェック
        for ext in ['csv', 'xml', 'txt']:
            annual_filename = f'{year}-all.{ext}'
            annual_path = year_dir / annual_filename
            
            if annual_path.exists():
                total_files += 1
            else:
                missing_files.append(f'{year}/{annual_filename}')
    
    return total_files, missing_files

def main():
    """メイン処理"""
    print('=== 古いファイル名削除・新ファイル名統一 ===')
    
    # 古いファイル名削除
    removed_count = remove_old_filename_links()
    print(f'\n削除完了: {removed_count}個の古いファイル名')
    
    # ダウンロード設定作成
    print('\n=== ダウンロード設定作成 ===')
    create_download_filename_htaccess()
    
    # 新ファイル名存在確認
    print('\n=== 新ファイル名存在確認 ===')
    total_files, missing_files = verify_new_filenames()
    
    print(f'新ファイル名形式: {total_files}個確認')
    
    if missing_files:
        print(f'欠落ファイル: {len(missing_files)}個')
        for missing in missing_files[:10]:  # 最初の10個だけ表示
            print(f'  - {missing}')
        if len(missing_files) > 10:
            print(f'  ... 他 {len(missing_files) - 10}個')
    else:
        print('✅ 全ファイル正常')
    
    print('\n✅ ファイル名統一完了')
    print('新しいファイル名形式に統一されました：')
    print('- 月別: 2026-01.csv, 2026-02.xml, 2026-03.txt')
    print('- 年間: 2026-all.csv, 2026-all.xml, 2026-all.txt')

if __name__ == '__main__':
    main()