#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园智慧信息网络中心问答助手 - 最终版服务器

此服务器用于提供问答助手的前端界面和相关资源。
特点：
- 使用8082端口，避免与其他服务冲突
- 提供详细的请求日志，方便调试和监控
- 完善的错误处理机制
- 支持中文路径和文件名
- 自动将根目录请求重定向到问答助手界面

使用方法:
1. 在命令行中导航到项目根目录
2. 运行: python final_server.py
3. 在浏览器中访问: http://localhost:8082/

上传到GitHub后，其他用户可以通过上述步骤轻松运行此服务器。
"""

import http.server
import socketserver
import os
import urllib.parse
import logging
from datetime import datetime
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 设置服务器端口
PORT = 8082

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"当前工作目录: {current_dir}")

class FinalHandler(http.server.SimpleHTTPRequestHandler):
    # 处理GET请求
    def do_GET(self):
        # 解析URL，分离路径和查询参数
        parsed_url = urllib.parse.urlparse(self.path)
        # 获取路径部分并解码URL编码的中文字符
        clean_path = urllib.parse.unquote(parsed_url.path)
        
        # 记录请求信息
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] 收到请求: {clean_path} 来自 {self.client_address[0]}:{self.client_address[1]}")
        
        # 如果请求根目录，则重定向到frontend目录下的完整问答助手界面.html
        if clean_path == '/':
            logger.info(f"请求根目录，将重定向到: /frontend/完整问答助手界面.html")
            # 修改self.path，只保留路径部分，不包含查询参数
            self.path = '/frontend/完整问答助手界面.html'
        else:
            # 更新self.path，只保留路径部分，不包含查询参数
            self.path = clean_path
        
        try:
            # 尝试提供请求的文件
            # 检查文件是否存在
            file_path = os.path.join(current_dir, self.path.lstrip('/'))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                logger.info(f"正在提供文件: {file_path}")
            else:
                logger.warning(f"文件不存在: {file_path}")
                
            # 调用父类的do_GET方法处理请求
            return super().do_GET()
        except Exception as e:
            error_msg = f"提供文件时出错: {str(e)}"
            logger.error(error_msg)
            # 使用英文错误消息避免编码问题
            self.send_error(500, "Internal Server Error")

    # 重写log_message方法，使用自定义日志系统
    def log_message(self, format, *args):
        return

    # 重写send_header方法，确保设置正确的Content-Type
    def send_header(self, keyword, value):
        # 特殊处理Content-Type，确保使用utf-8编码
        if keyword.lower() == 'content-type' and 'charset=' not in value.lower():
            value += '; charset=utf-8'
        super().send_header(keyword, value)

    # 重写send_response方法，添加自定义日志
    def send_response(self, code, message=None):
        # 记录响应状态
        logger.info(f"响应状态码: {code} {message or ''}")
        super().send_response(code, message)

if __name__ == "__main__":
    try:
        # 创建并启动服务器
        with socketserver.TCPServer(('', PORT), FinalHandler) as httpd:
            print(f"\n===== 校园智慧信息网络中心问答助手服务器 ======")
            print(f"服务器已成功启动")
            print(f"工作目录: {current_dir}")
            print(f"访问地址: http://localhost:{PORT}/")
            print(f"这将直接展示完整问答助手界面")
            print(f"\n服务日志:")
            print(f"=========================================")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n=========================================")
                print("服务器已停止")
                httpd.server_close()
    except Exception as e:
        error_msg = f"服务器启动失败: {str(e)}"
        logger.error(error_msg)
        print(f"\n错误: {error_msg}")
        print("请检查端口是否被占用，或者是否有其他系统限制。")
        print(f"尝试使用其他端口，请修改代码中的PORT变量（当前值: {PORT}）")