#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
from threading import Timer

PORT = 8081

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP请求处理器，禁用缓存"""

    def end_headers(self):
        """添加禁用缓存的HTTP头"""
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def open_browser():
    """延迟打开浏览器"""
    webbrowser.open(f'http://localhost:{PORT}/rental_viewer.html')

def start_server():
    """启动无缓存HTTP服务器"""
    os.chdir('/Users/mac/claude-project')

    with socketserver.TCPServer(("127.0.0.1", PORT), NoCacheHTTPRequestHandler) as httpd:
        print("🔄 VanPeople租房信息服务器 (无缓存版)")
        print("=" * 50)
        print(f"🚀 服务器地址: http://localhost:{PORT}")
        print(f"🌐 租房页面: http://localhost:{PORT}/rental_viewer.html")
        print(f"📁 服务目录: {os.getcwd()}")
        print("=" * 50)
        print("✨ 特性:")
        print("   • 禁用浏览器缓存，始终显示最新数据")
        print("   • 自动显示最新的抓取时间戳")
        print("   • 实时更新JSON数据")
        print("=" * 50)
        print("⌨️  按 Ctrl+C 停止服务器")
        print("=" * 50)

        # 2秒后自动打开浏览器
        Timer(2.0, open_browser).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 正在关闭服务器...")
            httpd.shutdown()
            print("✅ 服务器已关闭")

if __name__ == "__main__":
    try:
        start_server()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {PORT} 已被占用")
            print("🔧 解决方案:")
            print("   1. 关闭占用端口的程序")
            print(f"   2. 运行: lsof -ti:{PORT} | xargs kill -9")
            print("   3. 或者等待几秒钟后重试")
        else:
            print(f"❌ 启动失败: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")