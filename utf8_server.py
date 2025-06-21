#!/usr/bin/env python3
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
    
    # TCP_REUSEADDRを設定してアドレス再利用を許可
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", port), UTF8HTTPRequestHandler) as httpd:
        print(f"UTF-8対応サーバーをポート {port} で起動中...")
        httpd.serve_forever()
