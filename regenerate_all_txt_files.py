"""
全TXTファイルを詳細な内容で再生成
月別・年間すべてのTXTファイルを改善された形式で更新
"""

import json
from pathlib import Path

def generate_detailed_txt_from_json(json_path, txt_path):
    """JSONファイルから詳細なTXTファイルを生成"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    content = []
    
    if isinstance(data, dict) and 'months' in data:
        # 年間データの場合
        year = data['year']
        content.append(f"{year}年 暦データ完全ガイド")
        content.append("=" * 50)
        content.append("")
        
        # 基本統計
        holidays = []
        ichiryu_days = []
        kuubou_days = []
        rokuyo_stats = {'先勝': 0, '友引': 0, '先負': 0, '仏滅': 0, '大安': 0, '赤口': 0}
        weekend_count = 0
        total_days = 0
        
        for month_data in data['months']:
            for day_data in month_data['days']:
                total_days += 1
                if day_data.get('is_holiday'):
                    holidays.append({
                        'date': day_data['date'],
                        'name': day_data.get('holiday_name', ''),
                        'weekday': day_data['weekday']
                    })
                if day_data.get('is_ichiryu_manbai'):
                    ichiryu_days.append(day_data['date'])
                if day_data.get('is_kuubou'):
                    kuubou_days.append({
                        'date': day_data['date'],
                        'type': day_data.get('kuubou_type', ''),
                        'jikkan_junishi': day_data.get('jikkan_junishi', '')
                    })
                if day_data.get('is_weekend'):
                    weekend_count += 1
                
                rokuyo = day_data.get('rokuyo', '')
                if rokuyo in rokuyo_stats:
                    rokuyo_stats[rokuyo] += 1
        
        content.append("■ 基本統計")
        content.append(f"総日数: {total_days}日")
        content.append(f"祝日数: {len(holidays)}日")
        content.append(f"週末日数: {weekend_count}日")
        content.append(f"一粒万倍日: {len(ichiryu_days)}日")
        content.append(f"空亡日: {len(kuubou_days)}日")
        content.append("")
        
        content.append("■ 六曜分布")
        for rokuyo, count in rokuyo_stats.items():
            content.append(f"{rokuyo}: {count}日")
        content.append("")
        
        content.append("■ 祝日一覧")
        content.append("-" * 30)
        if holidays:
            for holiday in holidays:
                content.append(f"{holiday['date']} ({holiday['weekday']}) - {holiday['name']}")
        else:
            content.append("祝日なし")
        content.append("")
        
        content.append("■ 一粒万倍日一覧（開運・金運上昇の日）")
        content.append("-" * 40)
        if ichiryu_days:
            for i, date in enumerate(ichiryu_days):
                if i % 5 == 0 and i > 0:
                    content.append("")
                content.append(date + ("  " if (i + 1) % 5 != 0 else ""))
        else:
            content.append("該当日なし")
        content.append("")
        
        content.append("■ 空亡（天中殺）日一覧")
        content.append("-" * 30)
        if kuubou_days:
            for kuubou in kuubou_days:
                content.append(f"{kuubou['date']} - {kuubou['jikkan_junishi']} ({kuubou['type']})")
        else:
            content.append("該当日なし")
        content.append("")
        
        # データ項目説明
        content.append("■ 提供データ項目（39項目）")
        content.append("-" * 35)
        content.append("基本情報: 日付、曜日、祝日、六曜")
        content.append("開運情報: 一粒万倍日、ラッキーナンバー、パワーストーン")
        content.append("四柱推命: 十干十二支、五行、陰陽、動物、十二運、空亡")
        content.append("スピリチュアル: キーワード、瞑想テーマ、エネルギーアドバイス")
        content.append("ライフスタイル: 推奨茶、アロマ、音楽、食事、風水")
        content.append("占術: 占星術、タロット、クリスタルヒーリング")
        content.append("その他: 花言葉、名言、二十四節気、月相")
        
    else:
        # 月別データの場合
        if isinstance(data, dict):
            year = data.get('year', '')
            month = data.get('month', '')
            month_name = data.get('month_name_jp', '')
            
            content.append(f"{year}年{month}月({month_name}) 暦データ詳細")
            content.append("=" * 50)
            content.append("")
            
            if 'days' in data:
                holidays = []
                ichiryu_days = []
                kuubou_days = []
                taian_days = []
                butsumetsu_days = []
                weekend_days = []
                special_keywords = []
                power_stones = set()
                
                for day_data in data['days']:
                    date = day_data['date']
                    weekday = day_data.get('weekday', '')
                    rokuyo = day_data.get('rokuyo', '')
                    
                    if day_data.get('is_holiday'):
                        holidays.append(f"{date} ({weekday}) - {day_data.get('holiday_name', '')}")
                    if day_data.get('is_ichiryu_manbai'):
                        ichiryu_days.append(f"{date} ({weekday}) - {rokuyo}")
                    if day_data.get('is_kuubou'):
                        kuubou_days.append(f"{date} ({weekday}) - {day_data.get('jikkan_junishi', '')} ({day_data.get('kuubou_type', '')})")
                    if rokuyo == '大安':
                        taian_days.append(f"{date} ({weekday})")
                    if rokuyo == '仏滅':
                        butsumetsu_days.append(f"{date} ({weekday})")
                    if day_data.get('is_weekend'):
                        weekend_days.append(f"{date} ({weekday})")
                    
                    # スピリチュアル要素の収集
                    keyword = day_data.get('daily_keyword', '')
                    if keyword and len(keyword) > 5:  # 興味深いキーワードのみ
                        special_keywords.append(f"{date}: {keyword}")
                    
                    stone = day_data.get('power_stone', '')
                    if stone:
                        power_stones.add(stone)
                
                content.append("■ 月間統計")
                content.append(f"総日数: {len(data['days'])}日")
                content.append(f"祝日数: {len(holidays)}日")
                content.append(f"週末日数: {len(weekend_days)}日")
                content.append(f"一粒万倍日: {len(ichiryu_days)}日")
                content.append(f"空亡日: {len(kuubou_days)}日")
                content.append(f"大安日: {len(taian_days)}日")
                content.append(f"仏滅日: {len(butsumetsu_days)}日")
                content.append("")
                
                if holidays:
                    content.append("■ 祝日")
                    content.append("-" * 20)
                    content.extend(holidays)
                    content.append("")
                
                if ichiryu_days:
                    content.append("■ 一粒万倍日（開運・金運上昇）")
                    content.append("-" * 30)
                    content.extend(ichiryu_days)
                    content.append("")
                
                if taian_days:
                    content.append("■ 大安日（何事にも吉）")
                    content.append("-" * 25)
                    content.extend(taian_days)
                    content.append("")
                
                if kuubou_days:
                    content.append("■ 空亡日（天中殺・注意日）")
                    content.append("-" * 30)
                    content.extend(kuubou_days)
                    content.append("")
                
                if butsumetsu_days:
                    content.append("■ 仏滅日（慎重に行動）")
                    content.append("-" * 25)
                    content.extend(butsumetsu_days)
                    content.append("")
                
                # スピリチュアル情報
                if special_keywords:
                    content.append("■ 特別なメッセージ・キーワード")
                    content.append("-" * 35)
                    for keyword in special_keywords[:5]:  # 最大5個まで
                        content.append(keyword)
                    content.append("")
                
                if power_stones:
                    content.append("■ 今月のパワーストーン")
                    content.append("-" * 25)
                    content.append(", ".join(sorted(power_stones)))
                    content.append("")
                
                # データ項目説明
                content.append("■ 提供データ項目（39項目）")
                content.append("-" * 35)
                content.append("基本情報: 日付、曜日、祝日、六曜")
                content.append("開運情報: 一粒万倍日、ラッキーナンバー、パワーストーン")
                content.append("四柱推命: 十干十二支、五行、陰陽、動物、十二運、空亡")
                content.append("スピリチュアル: キーワード、瞑想テーマ、エネルギーアドバイス")
                content.append("ライフスタイル: 推奨茶、アロマ、音楽、食事、風水")
                content.append("占術: 占星術、タロット、クリスタルヒーリング")
                content.append("その他: 花言葉、名言、二十四節気、月相")
    
    # TXTファイル保存
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def regenerate_all_txt_files():
    """全TXTファイルを再生成"""
    
    generated_count = 0
    
    for year in range(2025, 2037):
        year_dir = Path(f'api/{year}')
        if not year_dir.exists():
            continue
            
        print(f'{year}年のTXTファイル再生成中...')
        
        # 月別TXTファイル再生成
        for month in range(1, 13):
            json_file = year_dir / f'{month:02d}.json'
            txt_file = year_dir / f'{year}-{month:02d}.txt'
            
            if json_file.exists():
                try:
                    generate_detailed_txt_from_json(json_file, txt_file)
                    generated_count += 1
                    print(f'  ✓ 再生成: {txt_file.name}')
                except Exception as e:
                    print(f'  ✗ エラー: {txt_file.name} - {e}')
        
        # 年間TXTファイル再生成
        annual_json = year_dir / 'all.json'
        annual_txt = year_dir / f'{year}-all.txt'
        
        if annual_json.exists():
            try:
                generate_detailed_txt_from_json(annual_json, annual_txt)
                generated_count += 1
                print(f'  ✓ 再生成: {annual_txt.name}')
            except Exception as e:
                print(f'  ✗ エラー: {annual_txt.name} - {e}')
    
    return generated_count

def main():
    """メイン処理"""
    print('=== 全TXTファイル詳細内容再生成 ===')
    
    generated_count = regenerate_all_txt_files()
    
    print(f'\n✅ 再生成完了: {generated_count}個のTXTファイル')
    print('詳細で有用な情報を含む形式に改善されました')

if __name__ == '__main__':
    main()