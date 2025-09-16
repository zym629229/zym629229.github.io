#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import signal
import sys
from threading import Timer

PORT = 8080

def signal_handler(sig, frame):
    """优雅关闭服务器"""
    print('\n🛑 正在关闭服务器...')
    print('✅ 服务器已安全关闭')
    sys.exit(0)

def open_browser():
    """延迟打开浏览器"""
    webbrowser.open(f'http://localhost:{PORT}/rental_viewer.html')

def start_server():
    """启动安全的HTTP服务器"""
    os.chdir('/Users/mac/claude-project')

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)

    with socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print("🔐 VanPeople租房信息安全服务器")
        print("=" * 50)
        print(f"🚀 服务器地址: http://localhost:{PORT}")
        print(f"🌐 租房页面: http://localhost:{PORT}/rental_viewer.html")
        print(f"📁 服务目录: {os.getcwd()}")
        print("=" * 50)
        print("🔒 安全提示:")
        print("   • 服务器仅绑定本地地址(127.0.0.1)")
        print("   • 外部网络无法访问")
        print("   • 只提供静态文件服务")
        print("   • 建议使用完毕后关闭服务器")
        print("=" * 50)
        print("⌨️  按 Ctrl+C 安全关闭服务器")
        print("=" * 50)

        # 2秒后自动打开浏览器
        Timer(2.0, open_browser).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 正在关闭服务器...")
            httpd.shutdown()
            print("✅ 服务器已安全关闭")

if __name__ == "__main__":
    try:
        start_server()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {PORT} 已被占用")
            print("🔧 解决方案:")
            print("   1. 关闭占用端口的程序")
            print("   2. 或者修改脚本使用其他端口")
            print(f"   3. 运行: lsof -ti:{PORT} | xargs kill -9")
        else:
            print(f"❌ 启动失败: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")