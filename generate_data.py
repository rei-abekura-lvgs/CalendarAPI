import json
import calendar
import datetime
from pathlib import Path

# --- 設定とマスターデータ ---

YEAR = 2025  # 生成する年

# 簡易的な祝日マスター (本来はライブラリなどを使う)
HOLIDAYS = {
    "01-01": "元日",
    "01-13": "成人の日",
    "02-11": "建国記念の日",
    "02-23": "天皇誕生日",
    "03-20": "春分の日",
    "04-29": "昭和の日",
    "05-03": "憲法記念日",
    "05-04": "みどりの日",
    "05-05": "こどもの日",
    "05-06": "振替休日",
    "07-21": "海の日",
    "08-11": "山の日",
    "09-15": "敬老の日",
    "09-23": "秋分の日",
    "10-13": "スポーツの日",
    "11-03": "文化の日",
    "11-23": "勤労感謝の日",
}

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

# --- メイン処理 ---
def generate_koyomi_data(year):
    print(f"{year}年の暦データを生成します...")
    output_dir = Path("api") / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)

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
            is_holiday = date_str in HOLIDAYS
            holiday_name = HOLIDAYS.get(date_str)

            # 簡易六曜
            rokuyo_index = (month + day) % 6
            rokuyo = ROKUYO_LIST[rokuyo_index]
            
            # その他の情報
            keyword = KEYWORDS[(day_of_year - 1) % len(KEYWORDS)]
            color = COLORS_OF_WEEK[weekday_index]
            tea = TEAS[(day_of_year - 1) % len(TEAS)]

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
                "season_24": None,  # 二十四節気は複雑なので今回は省略
                "moon_phase": "調査中",  # 月の満ち欠けも複雑なので今回は省略
                "daily_keyword": keyword,
                "color_of_the_day": color,
                "recommended_tea": tea
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
    generate_koyomi_data(YEAR)
    print("\nすべてのデータの生成が完了しました。")
    print("'api' ディレクトリの中身をGitHubリポジトリに配置してください。")
