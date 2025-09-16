#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
from threading import Timer

PORT = 8080

def open_browser():
    """延迟打开浏览器"""
    webbrowser.open(f'http://localhost:{PORT}/rental_viewer.html')

def start_server():
    """启动HTTP服务器"""
    os.chdir('/Users/mac/claude-project')

    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"🚀 服务器启动成功！")
        print(f"📍 服务器地址: http://localhost:{PORT}")
        print(f"🌐 租房信息页面: http://localhost:{PORT}/rental_viewer.html")
        print(f"📁 当前目录: {os.getcwd()}")
        print("=" * 60)
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)

        # 2秒后自动打开浏览器
        Timer(2.0, open_browser).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()