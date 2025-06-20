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

## User Preferences

- 日本語でのコミュニケーション
- JSON APIとして直接URLアクセス可能な形式を希望
- ドキュメントサイトは必須ではない
- 色はカラーコードではなく日本語の色名を希望
- キーワードはより気の利いた心に響く表現を希望
- 1ヶ月分のデータを一覧表示できる機能を希望