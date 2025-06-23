import json
import calendar
import datetime
from pathlib import Path

# --- 設定とマスターデータ ---

YEARS = list(range(2025, 2037))  # 2025年から2036年まで（12年分）

def calculate_ichiryu_manbai_days(year):
    """一粒万倍日を計算する"""
    ichiryu_days = []
    
    # 一粒万倍日の干支組み合わせ
    # 甲子、己巳、甲午、己亥、乙酉、庚寅、甲辰、己酉、庚子、乙巳
    # 簡易計算：月ごとの一粒万倍日パターン
    ichiryu_patterns = {
        1: [3, 6, 8, 15, 18, 20, 27, 30],    # 1月
        2: [2, 5, 12, 14, 19, 24, 26],       # 2月  
        3: [1, 8, 13, 16, 20, 25, 28],       # 3月
        4: [2, 5, 9, 17, 20, 29],            # 4月
        5: [2, 7, 14, 19, 26, 31],           # 5月
        6: [3, 8, 13, 18, 25, 30],           # 6月
        7: [5, 7, 12, 17, 24, 29],           # 7月
        8: [1, 8, 13, 16, 20, 25, 28],       # 8月
        9: [2, 9, 12, 17, 24, 29],           # 9月
        10: [1, 6, 9, 14, 21, 26],           # 10月
        11: [2, 5, 10, 13, 18, 25, 30],      # 11月
        12: [2, 7, 12, 15, 19, 27, 30]       # 12月
    }
    
    for month in range(1, 13):
        for day in ichiryu_patterns.get(month, []):
            try:
                date = datetime.date(year, month, day)
                ichiryu_days.append(date.strftime("%m-%d"))
            except ValueError:
                # 存在しない日付（例：2月30日）はスキップ
                continue
    
    return ichiryu_days

def get_jikkan_junishi(year, month, day):
    """十干十二支を計算"""
    # 十干（じっかん）
    jikkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 十二支（じゅうにし）
    junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 基準日からの日数を計算（1900年1月1日を基準とする）
    base_date = datetime.date(1900, 1, 1)
    current_date = datetime.date(year, month, day)
    days_diff = (current_date - base_date).days
    
    # 十干十二支のサイクル（60日周期）
    jikkan_index = (days_diff + 6) % 10  # 1900年1月1日は庚子なので調整
    junishi_index = (days_diff + 6) % 12
    
    return f"{jikkan[jikkan_index]}{junishi[junishi_index]}"

def get_holidays_for_year(year):
    """年別の祝日を計算（固定祝日と移動祝日の両方に対応）"""
    holidays = {}
    
    # 固定祝日
    fixed_holidays = {
        "01-01": "元日",
        "02-11": "建国記念の日", 
        "02-23": "天皇誕生日",
        "04-29": "昭和の日",
        "05-03": "憲法記念日",
        "05-04": "みどりの日",
        "05-05": "こどもの日",
        "08-11": "山の日",
        "11-03": "文化の日",
        "11-23": "勤労感謝の日"
    }
    holidays.update(fixed_holidays)
    
    # 移動祝日の計算
    import calendar
    
    # 成人の日（1月第2月曜日）
    first_monday = None
    for day in range(1, 8):
        if calendar.weekday(year, 1, day) == 0:  # 月曜日
            first_monday = day
            break
    if first_monday:
        adult_day = first_monday + 7
        holidays[f"01-{adult_day:02d}"] = "成人の日"
    
    # 海の日（7月第3月曜日）
    third_monday_july = None
    monday_count = 0
    for day in range(1, 32):
        if calendar.weekday(year, 7, day) == 0:  # 月曜日
            monday_count += 1
            if monday_count == 3:
                third_monday_july = day
                break
    if third_monday_july:
        holidays[f"07-{third_monday_july:02d}"] = "海の日"
    
    # 敬老の日（9月第3月曜日）
    third_monday_sept = None
    monday_count = 0
    for day in range(1, 31):
        if calendar.weekday(year, 9, day) == 0:  # 月曜日
            monday_count += 1
            if monday_count == 3:
                third_monday_sept = day
                break
    if third_monday_sept:
        holidays[f"09-{third_monday_sept:02d}"] = "敬老の日"
    
    # スポーツの日（10月第2月曜日）
    second_monday_oct = None
    monday_count = 0
    for day in range(1, 32):
        if calendar.weekday(year, 10, day) == 0:  # 月曜日
            monday_count += 1
            if monday_count == 2:
                second_monday_oct = day
                break
    if second_monday_oct:
        holidays[f"10-{second_monday_oct:02d}"] = "スポーツの日"
    
    # 春分の日・秋分の日は簡易計算（実際の計算は複雑）
    # 2025-2036年の近似値
    spring_equinox_days = {
        2025: 20, 2026: 20, 2027: 21, 2028: 20, 2029: 20, 2030: 20,
        2031: 21, 2032: 20, 2033: 20, 2034: 21, 2035: 21, 2036: 20
    }
    autumn_equinox_days = {
        2025: 23, 2026: 23, 2027: 23, 2028: 22, 2029: 23, 2030: 23,
        2031: 23, 2032: 22, 2033: 23, 2034: 23, 2035: 23, 2036: 22
    }
    
    if year in spring_equinox_days:
        holidays[f"03-{spring_equinox_days[year]:02d}"] = "春分の日"
    if year in autumn_equinox_days:
        holidays[f"09-{autumn_equinox_days[year]:02d}"] = "秋分の日"
    
    return holidays

ROKUYO_LIST = ["大安", "赤口", "先勝", "友引", "先負", "仏滅"]
WEEKDAY_LIST = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
COLORS_OF_WEEK = ["金色", "朱色", "空色", "若草色", "黄金色", "鋼青色", "深紅色"]
KEYWORDS = [
    "運命の扉が開く日", "宇宙からのメッセージ", "奇跡を呼ぶ波動", "龍神様のご加護", "金運上昇のサイン", 
    "恋愛運絶好調", "直感力が冴える", "隠れた才能開花", "人生の転機到来", "幸運の風が吹く", 
    "魂の成長期間", "エネルギー充電日", "新次元への扉", "守護霊のささやき", "願いが叶う予感", 
    "心のデトックス", "創造力爆発", "人との縁を結ぶ", "未来への種まき", "宝物発見の予感",
    "内なる光が輝く", "調和のメロディ", "自然の叡智授受", "知恵の泉湧出", "至福の時間軸",
    "運気上昇の兆し", "心の扉が開放", "宇宙との同調", "愛のバイブレーション", "豊かさの波動"
]
TEAS = [
    "アールグレイ", "カモミールティー", "ペパーミントティー", "緑茶", "ほうじ茶",
    "ジャスミンティー", "ルイボスティー", "ローズヒップティー", "白茶", "烏龍茶",
    "玄米茶", "抹茶", "柚子茶", "生姜茶", "黒豆茶"
]

# 追加データ
LUCKY_NUMBERS = list(range(1, 100))  # 1-99のラッキーナンバー
POWER_STONES = [
    "アメジスト", "ローズクォーツ", "クリスタル", "アクアマリン", "ガーネット",
    "ムーンストーン", "ラピスラズリ", "マラカイト", "オニキス", "シトリン",
    "ペリドット", "トルマリン", "オパール", "ターコイズ", "エメラルド"
]
AROMA_OILS = [
    "ラベンダー", "ユーカリ", "ローズマリー", "オレンジ", "レモングラス",
    "イランイラン", "サンダルウッド", "フランキンセンス", "ジャスミン", "ベルガモット",
    "ティーツリー", "ゼラニウム", "パチュリ", "シダーウッド", "カモミール"
]
MEDITATION_THEMES = [
    "感謝の瞑想", "慈悲の瞑想", "呼吸に集中", "マインドフルネス", "ボディスキャン",
    "愛と光の瞑想", "チャクラ調整", "グラウンディング", "エネルギー浄化", "未来創造",
    "過去の癒し", "内なる平和", "宇宙との繋がり", "直感力向上", "創造性開花"
]
FLOWER_MEANINGS = [
    "桜 - 精神の美", "梅 - 気品", "椿 - 控えめな素晴らしさ", "菊 - 高貴", "蓮 - 清らかな心",
    "薔薇 - 愛情", "向日葵 - 憧れ", "紫陽花 - 移り気", "牡丹 - 富貴", "百合 - 純粋",
    "カーネーション - 母の愛", "コスモス - 乙女の真心", "すずらん - 謙遜", "菜の花 - 快活", "藤 - 優しさ"
]
ENERGY_ADVICE = [
    "今日は新しい挑戦の時", "休息を大切にする日", "人との繋がりを深める日", "創造性を発揮する時",
    "内省の時間を作る日", "感謝を表現する日", "勇気を出して行動する時", "直感に従う日",
    "学びを深める好機", "愛を分かち合う日", "エネルギーを充電する時", "変化を受け入れる日",
    "夢を描く時間", "心を整理する日", "自然と触れ合う日"
]

# さらなる追加データ
ZODIAC_SIGNS = [
    "牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座",
    "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"
]
TAROT_CARDS = [
    "愚者 - 新しい始まり", "魔術師 - 創造力", "女教皇 - 直感", "女帝 - 豊穣", "皇帝 - 安定",
    "教皇 - 叡智", "恋人 - 選択", "戦車 - 意志力", "力 - 内なる強さ", "隠者 - 内省",
    "運命の輪 - 転機", "正義 - バランス", "吊られた男 - 犠牲", "死神 - 変容", "節制 - 調和",
    "悪魔 - 誘惑", "塔 - 変革", "星 - 希望", "月 - 幻想", "太陽 - 成功", "審判 - 再生", "世界 - 完成"
]
WISE_QUOTES = [
    "一歩一歩が大切な旅路", "今日という日は二度と来ない", "心の平安が真の豊かさ", "変化は成長の扉",
    "感謝の心が幸福を呼ぶ", "愛は最も強いエネルギー", "困難は成長のギフト", "今この瞬間が全て",
    "笑顔は心の太陽", "優しさは伝染する", "夢は現実の種", "勇気は恐れを超越する",
    "知恵は経験から生まれる", "調和は美の根源", "希望は明日への光", "慈悲は魂の栄養"
]
MUSIC_GENRES = [
    "クラシック", "ジャズ", "アンビエント", "ヒーリング", "ネイチャーサウンド",
    "瞑想音楽", "ピアノソロ", "オルゴール", "シンギングボウル", "チルアウト",
    "ボサノバ", "レゲエ", "フォーク", "インストゥルメンタル", "ワールドミュージック"
]
RECOMMENDED_FOODS = [
    "季節の野菜スープ", "玄米おにぎり", "緑黄色野菜サラダ", "蒸し魚", "豆腐料理",
    "発酵食品", "ナッツとドライフルーツ", "ハーブティーと蜂蜜", "旬の果物", "薬膳粥",
    "温野菜", "海藻料理", "きのこ類", "根菜の煮物", "自然食品"
]
CRYSTAL_HEALING = [
    "アメジスト - 心の浄化", "ローズクォーツ - 愛の波動", "クリアクォーツ - エネルギー増幅",
    "ブラックトルマリン - 邪気払い", "シトリン - 金運上昇", "ラピスラズリ - 真実の洞察",
    "ムーンストーン - 女性性", "ガーネット - 情熱", "アクアマリン - 平和", "ペリドット - 癒し",
    "オニキス - 意志力", "マラカイト - 変容", "ターコイズ - 護符", "オパール - 創造性", "エメラルド - 豊穣"
]
FENG_SHUI_ADVICE = [
    "玄関を清潔に保つ", "観葉植物で気の流れを良くする", "鏡で光を取り入れる", "水回りの掃除",
    "不要な物を手放す", "東向きに花を飾る", "ピンク色で恋愛運向上", "金色で金運アップ",
    "緑で健康運向上", "赤で活力を高める", "青で冷静さを保つ", "紫で精神性を高める",
    "オレンジで社交性向上", "黄色で明るさを増す", "白で清浄化"
]

# --- メイン処理 ---
def generate_koyomi_data(year):
    print(f"{year}年の暦データを生成します...")
    output_dir = Path("api") / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)

    # その年の祝日を取得
    holidays = get_holidays_for_year(year)
    
    # 一粒万倍日を取得
    ichiryu_days = calculate_ichiryu_manbai_days(year)

    # 全年データを格納するリスト
    all_data = {
        "year": year,
        "api_version": "v1",
        "generated_at": datetime.datetime.now().isoformat(),
        "months": []
    }

    for month in range(1, 13):
        month_data = {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "month_name_jp": [
                "1月", "2月", "3月", "4月", "5月", "6月",
                "7月", "8月", "9月", "10月", "11月", "12月"
            ][month - 1],
            "api_version": "v1",
            "generated_at": datetime.datetime.now().isoformat(),
            "days": []
        }
        
        # その月の日数を取得
        num_days = calendar.monthrange(year, month)[1]

        for day in range(1, num_days + 1):
            date = datetime.date(year, month, day)
            date_str = date.strftime("%m-%d")
            day_of_year = date.timetuple().tm_yday

            # 曜日
            weekday_index = date.weekday()  # 0:月曜, 6:日曜
            weekday_name = WEEKDAY_LIST[weekday_index]

            # 祝日
            is_holiday = date_str in holidays
            holiday_name = holidays.get(date_str)

            # 簡易六曜
            rokuyo_index = (month + day) % 6
            rokuyo = ROKUYO_LIST[rokuyo_index]
            
            # 一粒万倍日判定
            is_ichiryu_manbai = date_str in ichiryu_days
            
            # その他の情報
            keyword = KEYWORDS[(day_of_year - 1) % len(KEYWORDS)]
            color = COLORS_OF_WEEK[weekday_index]
            tea = TEAS[(day_of_year - 1) % len(TEAS)]
            
            # 十干十二支を追加
            jikkan_junishi = get_jikkan_junishi(year, month, day)
            
            # 追加データの生成
            lucky_number = LUCKY_NUMBERS[(day_of_year - 1) % len(LUCKY_NUMBERS)]
            power_stone = POWER_STONES[(day_of_year - 1) % len(POWER_STONES)]
            aroma_oil = AROMA_OILS[(day_of_year - 1) % len(AROMA_OILS)]
            meditation_theme = MEDITATION_THEMES[(day_of_year - 1) % len(MEDITATION_THEMES)]
            flower_meaning = FLOWER_MEANINGS[(day_of_year - 1) % len(FLOWER_MEANINGS)]
            energy_advice = ENERGY_ADVICE[(day_of_year - 1) % len(ENERGY_ADVICE)]
            
            # さらなる追加データ
            zodiac_sign = ZODIAC_SIGNS[(day_of_year - 1) % len(ZODIAC_SIGNS)]
            tarot_card = TAROT_CARDS[(day_of_year - 1) % len(TAROT_CARDS)]
            wise_quote = WISE_QUOTES[(day_of_year - 1) % len(WISE_QUOTES)]
            music_genre = MUSIC_GENRES[(day_of_year - 1) % len(MUSIC_GENRES)]
            recommended_food = RECOMMENDED_FOODS[(day_of_year - 1) % len(RECOMMENDED_FOODS)]
            crystal_healing = CRYSTAL_HEALING[(day_of_year - 1) % len(CRYSTAL_HEALING)]
            feng_shui_advice = FENG_SHUI_ADVICE[(day_of_year - 1) % len(FENG_SHUI_ADVICE)]

            day_info = {
                "day": day,
                "date": date.isoformat(),
                "weekday": weekday_name,
                "weekday_en": date.strftime("%A"),
                "weekday_short": date.strftime("%a"),
                "is_weekend": weekday_index >= 5,
                "is_holiday": is_holiday,
                "holiday_name": holiday_name,
                "rokuyo": rokuyo,
                "is_ichiryu_manbai": is_ichiryu_manbai,
                "jikkan_junishi": jikkan_junishi,
                "season_24": None,  # 二十四節気は複雑なので今回は省略
                "moon_phase": "調査中",  # 月の満ち欠けも複雑なので今回は省略
                "daily_keyword": keyword,
                "color_of_the_day": color,
                "recommended_tea": tea,
                "lucky_number": lucky_number,
                "power_stone": power_stone,
                "aroma_oil": aroma_oil,
                "meditation_theme": meditation_theme,
                "flower_of_the_day": flower_meaning,
                "energy_advice": energy_advice,
                "zodiac_influence": zodiac_sign,
                "tarot_card": tarot_card,
                "wise_quote": wise_quote,
                "recommended_music": music_genre,
                "recommended_food": recommended_food,
                "crystal_healing": crystal_healing,
                "feng_shui_tip": feng_shui_advice
            }
            month_data["days"].append(day_info)

        # 月ごとのJSONファイルを出力
        file_path = output_dir / f"{str(month).zfill(2)}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(month_data, f, ensure_ascii=False, indent=2)
            print(f"-> {file_path} を生成しました。")

        # 全年データにも追加
        all_data["months"].append(month_data)

    # 全年データのJSONファイルを出力
    all_file_path = output_dir / "all.json"
    with open(all_file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"-> {all_file_path} を生成しました。")

if __name__ == "__main__":
    for year in YEARS:
        print(f"\n=== {year}年のデータを生成中 ===")
        generate_koyomi_data(year)
    
    print(f"\n{len(YEARS)}年分のデータ生成が完了しました。")
    print("対象年:", ", ".join(map(str, YEARS)))
    print("'api' ディレクトリの中身をGitHubリポジトリに配置してください。")
