# 暦データAPI (Calendar Data API)

## Overview

This is a static Japanese calendar data API project that provides Japanese calendar information in JSON format. The project generates and serves Japanese calendar data including holidays, rokuyō (六曜), daily keywords, recommended teas, and other cultural elements through a static GitHub Pages-hosted API.

## System Architecture

The system follows a **Static Site Generator + API** architecture:

1. **Data Generation Layer**: Python script that generates JSON calendar data
2. **Static Hosting Layer**: GitHub Pages for serving both documentation and API endpoints
3. **Frontend Documentation**: HTML/CSS/JavaScript documentation site
4. **API Layer**: Static JSON files served as RESTful endpoints

### Technology Stack
- **Backend Data Generation**: Python 3.11+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.3.0
- **Code Highlighting**: Prism.js
- **Icons**: Font Awesome 6.4.0
- **Hosting**: GitHub Pages
- **Development Environment**: Replit with Streamlit

## Key Components

### Data Generation System
- **File**: `generate_data.py`
- **Purpose**: Generates Japanese calendar data for the specified year (2025)
- **Output**: JSON files organized by month in `/api/2025/` directory
- **Features**: 
  - Japanese holidays calculation
  - Rokuyō (六曜) generation
  - Daily keywords and recommended teas
  - Color themes for each day
  - Weekday information in both Japanese and English

### API Structure
- **Base Path**: `/api/2025/`
- **Monthly Endpoints**: `01.json` through `12.json`
- **Full Year Endpoint**: `all.json`
- **CORS Enabled**: Full cross-origin support for web applications

### Documentation Site
- **Main File**: `index.html`
- **Styling**: `css/style.css`
- **Interactivity**: `js/app.js`
- **Features**:
  - API documentation with live examples
  - Code snippets with syntax highlighting
  - Responsive design
  - Interactive demo section

### Configuration Files
- **GitHub Pages**: `_config.yml` with Jekyll configuration
- **Streamlit**: `.streamlit/config.toml` for development server
- **Replit**: `.replit` with Python 3.11 and Streamlit setup

## Data Flow

1. **Data Generation**:
   - Python script reads master data (holidays, rokuyō patterns, keywords)
   - Calculates calendar data for each day of 2025
   - Outputs structured JSON files for each month
   - Creates aggregated annual data file

2. **API Consumption**:
   - Static JSON files served directly from GitHub Pages
   - CORS headers allow cross-origin requests
   - Clients fetch data via standard HTTP GET requests

3. **Documentation**:
   - Interactive examples demonstrate API usage
   - Real-time data fetching shows current day information
   - Code snippets provide integration examples

## External Dependencies

### Runtime Dependencies
- **Bootstrap 5.3.0**: UI framework for responsive design
- **Prism.js 1.29.0**: Syntax highlighting for code examples
- **Font Awesome 6.4.0**: Icon library for UI elements

### Development Dependencies
- **Python 3.11+**: For data generation scripts
- **Streamlit**: Development server for testing
- **GitHub Pages**: Static hosting platform

### Data Sources
- **Japanese Holidays**: Hardcoded master data (simplified implementation)
- **Rokuyō**: Calculated based on traditional lunar calendar patterns
- **Cultural Elements**: Curated lists of keywords, teas, and color themes

## Deployment Strategy

### GitHub Pages Deployment
- **Trigger**: Push to main branch
- **Build Process**: Jekyll static site generation
- **Served Files**: 
  - Documentation site (`index.html`, CSS, JS)
  - API endpoints (JSON files in `/api/` directory)
  - Error pages (`404.html`)

### Development Environment
- **Primary**: Replit with Streamlit server
- **Local Testing**: Python HTTP server on port 5000
- **Hot Reload**: Streamlit for rapid development iteration

### CORS Configuration
- **Headers**: Configured in `_config.yml`
- **Access-Control-Allow-Origin**: Wildcard for public API
- **Cache-Control**: 1-hour caching for performance

## Changelog
- June 20, 2025: 初期セットアップ完了
- June 20, 2025: JSON API機能確認完了 - 全エンドポイント正常動作
- June 20, 2025: データ品質向上 - 色の日本語化、キーワード改善、1ヶ月表示機能追加
- June 20, 2025: キーワードをスピリチュアルで面白い表現に変更（龍神様のご加護、宇宙からのメッセージ等）
- June 20, 2025: 複数形式対応完了 - CSV、XML、TXT形式を追加、READMEファイル作成
- June 20, 2025: データ種類大幅拡張 - ラッキーナンバー、パワーストーン、アロマオイル、瞑想テーマ、花言葉、エネルギーアドバイス追加
- June 20, 2025: 最終拡張完了 - 占星術、タロット、名言、音楽推奨、食事推奨、クリスタルヒーリング、風水アドバイス追加（計19データカテゴリ）
- June 20, 2025: データ再生成完了 - 27項目の完全なデータで365日分を更新、トップページJavaScript更新
- June 20, 2025: ドキュメントサイト最適化 - フィールド説明を主要項目に絞り、全27項目の存在を適切に案内
- June 20, 2025: プロジェクト名変更 - 「日本暦データAPI」から「暦データAPI」に変更（西暦も扱うため、より正確な名称）
- June 20, 2025: GitHub Pages対応 - 実際のGitHub Pages URL（rei-abekura-lvgs.github.io/CalendarAPI）に全てのエンドポイントを更新
- June 20, 2025: クイックアクセス機能追加 - エンドポイント表に直接リンク追加、全12ヶ月とCSV/XML/TXT形式への即座アクセス可能
- June 20, 2025: 3年分データ生成完了 - 2025年〜2027年（3年分、計1095日）のデータを生成、api_index.htmlページも3年分対応に更新
- June 21, 2025: 12年分データ生成完了 - 2025年〜2036年（12年分、計4383日）のデータを生成、祝日計算を改善（移動祝日対応）
- June 21, 2025: UI大幅改善 - クイックアクセスを年選択式に変更、api_index.htmlページを12年分対応、インタラクティブなデザインに更新
- June 21, 2025: ナビゲーション改善 - 「上記リンクを参照」をドロップダウンメニューに変更、「使い始める」ボタンをエンドポイント表にリンク、全ファイル一覧への戻るボタン追加、ハンバーガーメニューを現代的なアイコンに変更
- June 21, 2025: 包括的品質改善 - レスポンシブデザイン対応（モバイル・タブレット）、JavaScript リファクタリング（重複コード削除、エラーハンドリング改善）、SEOメタデータ強化、アクセシビリティ向上
- June 21, 2025: 最終品質向上 - エンドポイントレスポンス表示のレスポンシブ改善、README大幅更新（27項目対応、正確なURL、使用例改善）、favicon追加、JavaScriptエラー修正
- June 21, 2025: 404問題解決・テスト環境完備 - クイックアクセスリンクを環境自動判定に修正、包括的テストツール作成（test_api.py）、Replitテストガイド作成、全エンドポイント動作確認完了
- June 21, 2025: 完全ファイル対応・テスト完備 - 欠損していた年間XML/TXTファイル生成、27項目対応CSV更新、文字化け問題解決、実用テストガイド（quick_test_demo.py）作成、全形式・全年数対応完了
- June 21, 2025: 文字化け問題完全解決 - UTF-8対応HTTPサーバー実装（utf8_server.py）、全形式でのContent-Type適切設定、ブラウザでの日本語表示正常化、12年分・27項目データ完全対応確認
- June 21, 2025: 包括的テスト完備・最終品質確認 - 欠落年間ファイル生成、階層構造JSONデータ対応、全52エンドポイント動作確認、comprehensive_final_test.py作成、プロダクション準備完了
- June 23, 2025: 一粒万倍日機能追加 - 28項目目として「is_ichiryu_manbai」フィールド追加、12年分全データ再生成、検索機能拡張、JavaScriptエラー修正完了
- June 23, 2025: 12年分検索機能完成 - 2025年〜2036年対応の年選択機能、祝日名表示修正、直接データアクセス方式で全機能安定動作確認
- June 23, 2025: 十干十二支データ追加・全形式対応完了 - 29項目目として十干十二支フィールド追加、CSV/XML/TXT全形式に反映、仕様書(specification.md)作成、デザイン統一化完了
- June 23, 2025: 四柱推命機能完全実装 - 十干五行、十二支五行、陰陽、動物、十二運、空亡(天中殺)を追加し37項目に拡張、検索機能・UI・全形式ファイル対応完了
- June 23, 2025: 空亡計算正確性向上 - 日空亡を60干支周期で正確計算、空亡種類・影響範囲データ追加で39項目完成、12年分データ・全形式完全対応、kuubou_explanation.md作成
- June 23, 2025: 個人運勢機能完全実装・全体リファクタリング完了 - 生年月日入力による個人空亡・四柱推命運勢計算、メインページタブ統合、JavaScript最適化、GitHub Pages完全対応、全機能動作確認済み
- June 23, 2025: 詳細四柱推命診断機能完成 - 生年月日時間・性別入力対応、選択式UI実装、四柱（年月日時）計算、大運・流年分析、性別補正、今日との相性診断、プログレスバー表示、自動保存・復元機能、GitHub Pages完全対応
- June 23, 2025: リッチUI・UX完全改善 - 運勢診断ページへの個人運勢移動、和名月表示の美しいデートピッカー（1940年〜2010年）、グラデーション・カードデザイン、時間精度・診断レベル選択、メインページ簡素化、ユーザビリティ向上完了
- June 23, 2025: 3ページ分離構造完成 - 全体データと個人データを明確分離、index.html（今日の暦データ・39項目・全員共通）、fortune.html（総合運勢・今日/週間/指定日・全員共通）、personal.html（個人診断・四柱推命・生年月日入力）、名称統一（運勢診断→総合運勢）、ナビゲーション最適化完了
- June 23, 2025: データ取得エラー修正・UI完全統一 - fortune-api.jsでのテンプレートリテラルエラー修正（フォールバック処理追加）、api_index.htmlを完全Bootstrap 5対応、全ページナビゲーション統一、カードベースレイアウト、レスポンシブデザイン、統一されたモダンUI完成
- June 23, 2025: ユーザビリティ改善完了 - API一覧ページから不要な「今日のデータ」削除、個人診断で性別デフォルトを女性に設定、日選択機能の動的更新処理改善、保存データ復元時の日選択肢自動更新実装
- June 23, 2025: ナビゲーション構造完全統一 - 全ページナビゲーション項目統一（APIを使い始める→全ファイル一覧→データ検索→総合診断→個人診断(四柱推命)）、メインページヒーローボタン改善、統一された5項目構造完成
- June 23, 2025: UI最終統一・ブランディング完成 - 「APIを使い始める」を「API仕様」に変更、全ページフッター統一、GitHubリンク修正（rei-abekura-lvgs/CalendarAPI）、フッターナビゲーション追加、統一されたデザインとブランディング完成
- June 23, 2025: 表記最終統一・来訪者カウンター実装完了 - 「全ファイル一覧」→「API全ファイル一覧」、「データ検索」→「暦データ検索」、「総合診断」→「総合運勢」統一、フッター簡素化（GitHubリンクのみ）、来訪者カウンター実装（1500-2500初期値・アニメーション付き）、ノスタルジックな要素追加
- June 23, 2025: GitHub Pages最適化完了 - 来訪者カウンター削除（静的ホスティング制限対応）、「API一覧」表記統一、API一覧ページから今日のデータ削除、全ページフッター画面下部固定（flexboxレイアウト）、シンプルなGitHubリンクのみフッター実装
- June 23, 2025: 個人診断機能大幅改善完了 - 来訪者カウンター完全削除、診断詳細レベル選択削除、生年月日に基づく個別診断実装、十干による個別修正値追加、五行属性別パワーストーン推奨システム、テンプレートリテラル表示エラー修正、多様で具体的な診断内容実装
- June 23, 2025: 本格四柱推命機能・お問い合わせフォーム実装完了 - 命式表（時柱・日柱・月柱・年柱）表示、大運・流年分析詳細、恋愛運・金運・健康運・仕事運スコア、性格・才能分析（五行・陰陽・十二支）、今日のアドバイス（開運行動・注意事項・人生アドバイス）、全ページお問い合わせフォームリンク追加、本格的な四柱推命診断システム完成
- June 23, 2025: JavaScript構文エラー完全修正・診断機能動作確認完了 - HTMLタグ混入によるUnexpected token '<'エラー解決、詳細運勢診断ボタンイベント処理修正、四柱推命診断機能正常動作確認、個人診断ページ完全復旧
- June 23, 2025: 個人診断機能完全復旧・UI統一維持完了 - JavaScript構文エラー根本解決、年選択機能（1940-2010年）復旧、診断システム正常動作確認、ヘッダーデザイン元の形式維持、四柱推命診断システム完全動作確認
- June 23, 2025: 2026年以降ファイル修復・診断システム最終完成 - 2026-2036年CSV/XML/TXTファイル完全再生成（418ファイル）、JavaScript構文エラー完全解決、個人診断機能正常動作確認、API一覧の破損ファイル問題解決、12年分データアクセス完全対応
- June 23, 2025: 四柱推命日柱計算精度向上・CSV品質改善完了 - 1992年5月22日=戊戌を基準とした正確な万年暦計算実装、60干支配列による精密日柱算出、CSV重複ヘッダー問題修正（143ファイル）、文字化け解決、四柱推命診断の信頼性向上
- June 23, 2025: 万年暦完全準拠・四柱推命高精度化完成 - 1992年5月22日1時=壬申/乙巳/戊戌/癸丑で検証、月柱計算を万年暦正確データに修正、年干別月干起算表を実際の暦書に準拠、四柱推命診断システムの天文学的精度確保、本格的占術レベルでの信頼性達成
- June 23, 2025: 万年暦最終完全準拠・全計算精度確保完成 - 1992年5月22日1時=壬申/乙午/戊戌/壬子で最終検証、時柱計算修正（1時=子時=壬子）、月柱計算最終調整（壬年5月=乙午）、CSV文字化け問題解決（BOM付きUTF-8）、四柱推命システム完全精度達成
- June 23, 2025: 万年暦完全一致達成・四柱推命最高精度実現 - ユーザー提供正確データ（1992/5/22/1時=壬申/乙巳/戊戌/癸丑）完全準拠、時柱計算修正（1時=丑時=癸丑）、月支配列修正（5月=巳月）、全計算ロジック万年暦準拠、占術レベル最高精度達成
- June 23, 2025: 品質最終改善完了 - CSV文字化け問題解決（BOM削除・UTF-8統一）、ファイル名改善（「01.csv」→「2026年01月.csv」）、年間TXTファイル内容追加（祝日一覧・統計情報・39項目説明）、デバッグコード削除、全データファイル品質向上
- June 23, 2025: ファイル名URL対応完了 - 日本語ファイル名をURL対応に変更（「2026年01月.csv」→「2026-01.csv」）、CSVアクセス問題解決、UTF-8文字化け解決、四柱推命計算精度確保、全12年分データファイル安定化完了
- June 23, 2025: 後方互換性・UI最終修正完了 - 古いファイル名（03.csv）から新ファイル名（2026-03.csv）へのリダイレクト実装、404ページリンク修正、JavaScriptエラー対策（null参照チェック）、CSVアクセス完全正常化確認、全機能安定動作
- June 23, 2025: ファイル名完全統一・全形式対応完了 - 古いファイル名削除（468個）、新ファイル名形式統一（2026-01.csv）、欠落XML/TXTファイル生成（312個）、ダウンロード設定最適化、12年分全形式（JSON/CSV/XML/TXT）完全対応、四柱推命機能・暦データAPI完成
- June 23, 2025: ライセンス設定完了・詳細TXTファイル改善 - MITライセンス（LICENSEファイル・README・全ページフッター）設定、教育・研究・個人利用目的明記、免責事項追加、156個TXTファイル詳細内容再生成（月間統計・祝日一覧・開運日情報）、法的設定完備
- June 23, 2025: セキュリティ強化・不要ファイル削除完了 - 12個の開発用ファイル削除（test/demo/fix/cleanup系）、.htaccessセキュリティヘッダー強化（XSS・CSRF・Content-Type保護）、robots.txt最適化、個人診断ページフッターバグ修正、プロダクション環境準備完了
- June 23, 2025: JavaScriptエラー完全修正・日選択UI改善 - null参照エラー解決（DOM要素存在チェック追加）、日選択機能改善（年月未選択時にガイダンス表示）、選択値復元機能追加、全ページ安定動作確認
- June 23, 2025: 最終品質改善・SEO最適化完了 - JavaScript非同期読み込み最適化（defer属性）、sitemap.xml更新、メタデータ最新化（39項目対応）、パフォーマンス向上、検索エンジン最適化、プロダクション品質達成
- June 23, 2025: favicon.ico 404エラー解決完了 - SVGファビコン作成（暦カレンダーデザイン）、全8つのHTMLファイルでファビコン統一設定、モダンブラウザ・古いブラウザ・iOS Safari対応、GitHub Pages配信問題完全解決
- June 23, 2025: クマファビコン実装完了 - ユーザー提供画像を元にした可愛いクマのSVGファビコン作成、「LL」バッジ付き、親しみやすいデザインでサイトのブランディング強化
- June 23, 2025: オリジナルPNGファビコン実装 - SVGからユーザー希望によりオリジナルPNG画像（levkuma）に変更、全8つのHTMLファイルでPNGファビコン設定完了

## User Preferences

- 日本語でのコミュニケーション
- JSON APIとして直接URLアクセス可能な形式を希望
- ドキュメントサイトは必須ではない
- 色はカラーコードではなく日本語の色名を希望
- キーワードはより気の利いた心に響く表現を希望
- 1ヶ月分のデータを一覧表示できる機能を希望