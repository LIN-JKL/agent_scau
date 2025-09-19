#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园智慧信息网络中心问答助手 - 静态文件服务器

此服务器用于提供问答助手的前端界面和相关资源。
默认使用8081端口，如果端口被占用，可以修改PORT变量。

使用方法:
1. 在命令行中导航到项目根目录
2. 运行: python simple_server.py
3. 在浏览器中访问: http://localhost:8081/
"""

import http.server
import socketserver
import os
import urllib.parse

# 设置服务器端口
# 如果端口被占用，可以修改为其他可用端口
PORT = 8081

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    # 处理GET请求
    def do_GET(self):
        # 解析请求路径
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # 如果请求根目录，则重定向到frontend目录下的完整问答助手界面.html
        if path == '/':
            self.path = '/frontend/完整问答助手界面.html'
            print(f"请求根目录，重定向到: {self.path}")
        
        try:
            # 尝试提供请求的文件
            return super().do_GET()
        except Exception as e:
            print(f"提供文件时出错: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    # 重写log_message方法，避免重复输出
    def log_message(self, format, *args):
        return

# 创建并启动服务器
if __name__ == "__main__":
    with socketserver.TCPServer(('', PORT), SimpleHandler) as httpd:
        print(f"\n简单静态文件服务器已启动")
        print(f"工作目录: {current_dir}")
        print(f"访问地址: http://localhost:{PORT}/")
        print(f"这将直接展示frontend/完整问答助手界面.html文件")
        print("按Ctrl+C停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
            httpd.server_close()