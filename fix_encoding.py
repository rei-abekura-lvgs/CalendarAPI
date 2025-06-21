#!/usr/bin/env python3
"""
TXTファイルの文字化け問題を修正

HTTPサーバーがtext/plainファイルを正しいエンコーディングで送信するよう設定を調整
"""

import os
import mimetypes
from pathlib import Path

def fix_mime_types():
    """MIMEタイプとエンコーディングを修正"""
    # UTF-8でのtext/plainを強制
    mimetypes.add_type('text/plain; charset=utf-8', '.txt')
    print("MIMEタイプを修正しました")

def create_htaccess():
    """Apache用の.htaccessファイルを作成（GitHub Pages用）"""
    htaccess_content = """
# UTF-8エンコーディングを強制
AddDefaultCharset UTF-8

# TXTファイルのMIMEタイプを設定
<Files "*.txt">
    ForceType "text/plain; charset=utf-8"
</Files>

# その他のテキストファイル
<Files "*.csv">
    ForceType "text/csv; charset=utf-8"
</Files>

<Files "*.xml">
    ForceType "application/xml; charset=utf-8"
</Files>

# CORSヘッダー
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type"
</IfModule>
"""
    
    with open('.htaccess', 'w', encoding='utf-8') as f:
        f.write(htaccess_content.strip())
    
    print(".htaccessファイルを作成しました")

def create_simple_server():
    """UTF-8対応のシンプルHTTPサーバーを作成"""
    server_content = """#!/usr/bin/env python3
import http.server
import socketserver
import mimetypes
import os

class UTF8HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # UTF-8エンコーディングを強制
        if self.path.endswith('.txt'):
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
        elif self.path.endswith('.csv'):
            self.send_header('Content-Type', 'text/csv; charset=utf-8')
        elif self.path.endswith('.xml'):
            self.send_header('Content-Type', 'application/xml; charset=utf-8')
        
        # CORS対応
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        super().end_headers()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    with socketserver.TCPServer(("0.0.0.0", port), UTF8HTTPRequestHandler) as httpd:
        print(f"UTF-8対応サーバーをポート {port} で起動中...")
        httpd.serve_forever()
"""
    
    with open('utf8_server.py', 'w', encoding='utf-8') as f:
        f.write(server_content)
    
    os.chmod('utf8_server.py', 0o755)
    print("UTF-8対応サーバー（utf8_server.py）を作成しました")

def test_encoding_fix():
    """エンコーディング修正をテスト"""
    import requests
    import time
    
    print("エンコーディング修正をテスト中...")
    
    try:
        # 少し待ってからテスト
        time.sleep(1)
        
        response = requests.get('http://localhost:5000/api/2025/01.txt')
        
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Encoding: {response.encoding}")
        
        # 正しく日本語が読めるかテスト
        text = response.text
        if '月' in text and '年' in text and not '\\x' in repr(text[:100]):
            print("✅ 文字化け修正成功")
            print(f"サンプル: {text[:100]}...")
        else:
            print("❌ 文字化けが残っています")
            print(f"サンプル: {repr(text[:100])}")
            
    except Exception as e:
        print(f"テストエラー: {e}")

def main():
    """メイン修正処理"""
    print("TXTファイル文字化け修正ツール")
    print("=" * 40)
    
    fix_mime_types()
    create_htaccess()
    create_simple_server()
    
    print("\n修正完了!")
    print("\n次のステップ:")
    print("1. ワークフローを再起動")
    print("2. または: python utf8_server.py でUTF-8サーバー起動")
    print("3. ブラウザでTXTファイルをテスト")

if __name__ == "__main__":
    main()