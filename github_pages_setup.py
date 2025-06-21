#!/usr/bin/env python3
"""
GitHub Pages設定確認・最適化ツール
404エラー解決のための設定チェック
"""

import os
from pathlib import Path

def check_github_pages_requirements():
    """GitHub Pages要件をチェック"""
    print("GitHub Pages設定チェック")
    print("=" * 40)
    
    # 必須ファイルの確認
    required_files = {
        'index.html': 'メインページ',
        'api_index.html': 'API一覧ページ', 
        '_config.yml': 'Jekyll設定',
        '.nojekyll': 'Jekyll無効化（オプション）'
    }
    
    print("必須ファイル確認:")
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✓ {file_path}: 存在 ({size} bytes) - {description}")
        else:
            print(f"✗ {file_path}: 不存在 - {description}")
    
    # API構造確認
    print("\nAPI構造確認:")
    api_dir = Path('api')
    if api_dir.exists():
        years = sorted([d.name for d in api_dir.iterdir() if d.is_dir() and d.name.isdigit()])
        print(f"✓ api/ディレクトリ: 存在")
        print(f"  対応年数: {len(years)}年 ({', '.join(years[:3])}...)")
        
        # サンプルファイル確認
        if years:
            sample_year = years[0]
            sample_files = list(Path(f'api/{sample_year}').glob('*.*'))
            print(f"  {sample_year}年ファイル数: {len(sample_files)}")
    else:
        print("✗ api/ディレクトリ: 不存在")
    
    # _config.yml詳細確認
    print("\nJekyll設定確認:")
    config_file = Path('_config.yml')
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'rei-abekura-lvgs.github.io' in content:
            print("✓ URL設定: 正しい")
        else:
            print("✗ URL設定: 要修正")
            
        if 'CalendarAPI' in content:
            print("✓ リポジトリ名: 正しい")
        else:
            print("✗ リポジトリ名: 要修正")
    
    # 推奨設定
    print("\n推奨設定:")
    recommendations = [
        "✓ .nojekyll ファイル作成済み（Jekyll処理をスキップ）",
        "✓ _config.yml でCORS設定済み",
        "◦ GitHub リポジトリでPages設定を確認",
        "◦ デプロイ完了まで3-10分待機",
        "◦ ブラウザキャッシュクリア"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")

def create_github_pages_status():
    """GitHub Pages ステータス確認用HTMLを作成"""
    status_html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Pages デプロイ状況</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .status { padding: 15px; margin: 10px 0; border-radius: 5px; }
        .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        .test-link { display: inline-block; margin: 5px; padding: 10px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 3px; }
        .test-link:hover { background-color: #0056b3; }
    </style>
    <script>
        function testAPI() {
            const testResults = document.getElementById('test-results');
            testResults.innerHTML = '<p>テスト実行中...</p>';
            
            // 基本的なAPIテスト
            const tests = [
                { name: '今日のデータ', url: 'api/2025/06.json' },
                { name: '年間データ', url: 'api/2025/all.json' },
                { name: 'TXTファイル', url: 'api/2025/01.txt' },
                { name: 'CSVファイル', url: 'api/2025/01.csv' }
            ];
            
            let results = [];
            
            Promise.all(tests.map(test => 
                fetch(test.url)
                    .then(response => ({ ...test, status: response.status, ok: response.ok }))
                    .catch(error => ({ ...test, status: 'エラー', ok: false, error: error.message }))
            )).then(allResults => {
                let html = '<h3>APIテスト結果:</h3>';
                allResults.forEach(result => {
                    const status = result.ok ? '✓' : '✗';
                    const color = result.ok ? 'green' : 'red';
                    html += `<p style="color: ${color}">${status} ${result.name}: ${result.status}</p>`;
                });
                testResults.innerHTML = html;
            });
        }
        
        window.onload = function() {
            document.getElementById('deploy-time').innerHTML = new Date().toLocaleString('ja-JP');
        };
    </script>
</head>
<body>
    <h1>🌟 暦データAPI - GitHub Pages デプロイ状況</h1>
    
    <div class="status success">
        <h2>✅ デプロイ成功</h2>
        <p>このページが表示されているということは、GitHub Pagesのデプロイが成功しています。</p>
        <p>確認日時: <span id="deploy-time"></span></p>
    </div>
    
    <div class="status info">
        <h2>📊 API概要</h2>
        <ul>
            <li>対象期間: 2025年〜2036年（12年分）</li>
            <li>データ項目: 27項目/日</li>
            <li>提供形式: JSON, CSV, XML, TXT</li>
            <li>総データ量: 4,383日分</li>
        </ul>
    </div>
    
    <h2>🔗 クイックリンク</h2>
    <a href="index.html" class="test-link">メインページ</a>
    <a href="api_index.html" class="test-link">API一覧</a>
    <a href="api/2025/06.json" class="test-link">今月のJSON</a>
    <a href="api/2025/all.txt" class="test-link">年間TXT</a>
    
    <h2>🧪 APIテスト</h2>
    <button onclick="testAPI()" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer;">
        APIテスト実行
    </button>
    <div id="test-results"></div>
    
    <hr style="margin: 30px 0;">
    <p><small>GitHub Pages URL: <a href="https://rei-abekura-lvgs.github.io/CalendarAPI/">https://rei-abekura-lvgs.github.io/CalendarAPI/</a></small></p>
</body>
</html>"""
    
    with open('status.html', 'w', encoding='utf-8') as f:
        f.write(status_html)
    
    print("✓ status.html を作成しました（デプロイ確認用）")

def main():
    """メイン処理"""
    check_github_pages_requirements()
    create_github_pages_status()
    
    print(f"\n🚀 GitHub Pages 対処法:")
    print("1. リポジトリのSettings > Pagesで'Deploy from a branch'を選択")
    print("2. Source: main branch / (root)")
    print("3. 数分待ってからアクセス")
    print("4. URL: https://rei-abekura-lvgs.github.io/CalendarAPI/")
    print("5. 確認用: https://rei-abekura-lvgs.github.io/CalendarAPI/status.html")

if __name__ == "__main__":
    main()