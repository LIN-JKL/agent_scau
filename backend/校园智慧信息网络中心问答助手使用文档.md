import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import random
import os
import json

# 全局变量用于存储模板和数据
templates = {}
faqs = []
knowledge_base = {}
responses = {}

# 初始化数据
def init_data():
    global knowledge_base, faqs, responses
    
    # 加载知识库数据
    knowledge_base = {
        "账号服务": "提供校园网账号、电子邮箱账号等各类账号的申请、查询、修改和注销等服务。",
        "网络服务": "提供校园网接入、网络故障报修、固定IP申请等服务。",
        "新生服务": "为新生提供校园网络开通、账号激活等服务指南。",
        "技术服务": "提供各类系统和设备的技术支持、咨询和培训服务。"
    }
    
    # 预设的常见问题
    faqs = [
        {"id": 1, "question": "如何申请校园网账号？", "category": "账号服务"},
        {"id": 2, "question": "校园网出现故障怎么办？", "category": "网络服务"},
        {"id": 3, "question": "新生如何开通校园网络？", "category": "新生服务"},
        {"id": 4, "question": "如何申请固定IP地址？", "category": "网络服务"},
        {"id": 5, "question": "校园卡丢失了怎么处理？", "category": "账号服务"}
    ]
    
    # 预设的响应
    responses = {
        "校园网账号": "校园网账号申请流程：1. 访问信息网络中心官网；2. 点击'账号服务'；3. 选择'校园网账号申请'；4. 填写个人信息并提交；5. 等待审核通过。",
        "网络故障": "校园网故障报修方式：1. 拨打服务热线8888-1234；2. 登录信息网络中心公众号进行线上报修；3. 前往信息楼101室现场报修。",
        "新生网络": "新生开通校园网络流程：1. 凭学生证和身份证到信息网络中心服务大厅；2. 填写《校园网络服务申请表》；3. 缴纳相关费用；4. 工作人员现场开通服务。",
        "固定IP": "🏢 固定IP申请流程：\n\n1. 登录校园网络服务平台\n2. 在「服务申请」中选择「固定IP绑定」\n3. 上传设备MAC地址\n4. 等待审核\n\n咨询电话：8888-1234",
        "校园卡丢失": "校园卡丢失处理：1. 立即通过校园卡服务平台或电话挂失；2. 携带本人身份证到校园卡服务中心补办；3. 缴纳补办费用20元。",
        "工作时间": "信息网络中心工作时间：周一至周五 8:00-17:30，周六 9:00-15:00，周日休息。"
    }
    
    # 初始化HTML模板
    init_templates()

# 处理用户问题的函数
def process_query(user_query):
    # 默认回复
    default_response = "感谢您的咨询。我们已记录您的问题，信息网络中心的工作人员将尽快与您联系。如需紧急帮助，请拨打服务热线8888-1234。"
    
    # 查找匹配的响应
    for key, response in responses.items():
        if key in user_query:
            return response
    
    # 检查是否有知识库中的内容匹配
    for title, content in knowledge_base.items():
        if title in user_query:
            return content
    
    # 如果没有匹配项，返回默认回复
    return default_response

# 初始化HTML模板
def init_templates():
    global templates
    
    # HTML模板字符串
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>校园智慧信息网络中心问答助手</title>
    <style>
        /* 全局样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Microsoft YaHei', sans-serif;
        }
        
        body {
            background-color: #f0f5f0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: url('image.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        
        /* 容器样式 */
        .container {
            width: 100%;
            max-width: 1200px;
            height: 90vh;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            box-shadow: 0 5px 30px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }
        
        /* 装饰元素 */
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #4CAF50, #8BC34A, #CDDC39);
        }
        
        /* 头部样式 */
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 80% 30%, rgba(255, 255, 255, 0.15) 0%, transparent 25%),
                radial-gradient(circle at 30% 80%, rgba(255, 255, 255, 0.12) 0%, transparent 22%),
                radial-gradient(circle at 90% 90%, rgba(255, 255, 255, 0.1) 0%, transparent 18%);
            z-index: 0;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 10px;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }
        
        .header p {
            position: relative;
            z-index: 1;
        }
        
        /* 主内容区域 */
        .main-content {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        /* 左侧面板 */
        .left-panel {
            width: 250px;
            background-color: rgba(248, 249, 250, 0.9);
            border-right: 1px solid #e9ecef;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }
        
        .category-title {
            padding: 15px;
            font-weight: bold;
            color: #495057;
            background-color: #e9ecef;
            border-bottom: 1px solid #dee2e6;
            font-size: 14px;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .faq-list {
            padding: 10px;
        }
        
        .faq-item {
            padding: 10px 15px;
            margin-bottom: 5px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            border: 1px solid transparent;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .faq-item:hover {
            background-color: #e8f5e9;
            border-color: #c8e6c9;
            transform: translateX(5px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* 右侧聊天区域 */
        .right-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        /* 聊天消息区域 */
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: rgba(255, 255, 255, 0.7);
            position: relative;
        }
        
        .chat-messages::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.5);
            z-index: 0;
        }
        
        .chat-messages > div {
            position: relative;
            z-index: 1;
        }
        
        /* 消息样式 */
        .message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            animation: fadeIn 0.3s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            align-items: flex-end;
        }
        
        .message.bot {
            align-items: flex-start;
        }
        
        .message-content {
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 12px;
            word-wrap: break-word;
            position: relative;
        }
        
        .message.user .message-content {
            background: white;
            color: #333;
            border: 1px solid #ddd;
            border-bottom-right-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #ddd;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        /* 头像样式 */
        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            margin-bottom: 5px;
            background-color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
        }
        
        .message.user .message-avatar {
            background-color: #4CAF50;
            color: white;
        }
        
        .message.bot .message-avatar {
            background-color: #8BC34A;
            color: white;
        }
        
        .message-time {
            font-size: 11px;
            color: #6c757d;
            margin-top: 5px;
        }
        
        /* 输入区域样式 */
        .chat-input {
            padding: 15px;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.95);
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 20px;
            border: 1px solid #dee2e6;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s ease;
        }
        
        .chat-input input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }
        
        .chat-input button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #4CAF50, #8BC34A);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        .chat-input button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .chat-input button:active {
            transform: translateY(0);
        }
        
        /* 正在输入状态 */
        .typing {
            padding: 10px 15px;
            color: #6c757d;
            font-style: italic;
        }
        
        /* 服务信息 */
        .service-info {
            padding: 15px;
            background-color: #e8f5e9;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #4CAF50;
        }
        
        /* 输入状态动画 */
        .typing-dots {
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #6c757d;
            animation: typing 1.4s infinite both;
        }
        
        .typing-dots span:nth-child(1) {
            animation-delay: 0s;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0% {
                transform: translateY(0);
                opacity: 0.7;
            }
            50% {
                transform: translateY(-5px);
                opacity: 1;
            }
            100% {
                transform: translateY(0);
                opacity: 0.7;
            }
        }
        
        /* 动态卡片样式 */
        .dynamic-card {
            margin-top: 10px;
            border: 2px dashed #a7f3d0;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
            background-color: white;
        }
        
        .dynamic-card:hover {
            border-color: #4ade80;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .card-header {
            padding: 12px 15px;
            font-weight: bold;
            background-color: rgba(34, 197, 94, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background-color 0.3s ease;
        }
        
        .dynamic-card:hover .card-header {
            background-color: rgba(34, 197, 94, 0.15);
        }
        
        .card-arrow {
            transition: transform 0.3s ease;
            font-size: 14px;
            color: #16a34a;
        }
        
        .card-content.hidden {
            display: none;
        }
        
        .card-content {
            padding: 15px;
            background-color: white;
            animation: fadeIn 0.3s ease;
        }
        
        /* 弹跳动画 */
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        .card-content ul, .card-content ol {
            margin: 0;
            padding-left: 20px;
        }
        
        .card-content li {
            margin-bottom: 8px;
            line-height: 1.6;
        }
        
        .status-bar {
            margin-top: 15px;
            height: 10px;
            background: #e5e7eb;
            border-radius: 5px;
            position: relative;
            overflow: hidden;
        }
        
        .progress {
            height: 100%;
            background: linear-gradient(90deg, #16a34a, #4ade80);
            border-radius: 5px;
            transition: width 1s ease-in-out;
            position: relative;
        }
        
        .progress::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .status-bar span {
            position: absolute;
            bottom: -20px;
            right: 0;
            font-size: 12px;
            color: #6c757d;
        }
        
        /* 可爱的装饰元素 */
        .decorator {
            position: absolute;
            pointer-events: none;
            z-index: 0;
            opacity: 0.5;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .main-content {
                flex-direction: column;
            }
            
            .left-panel {
                width: 100%;
                height: 200px;
                border-right: none;
                border-bottom: 1px solid #e9ecef;
            }
            
            .message-content {
                max-width: 85%;
            }
        }
        
        /* 链接样式 */
        a {
            color: #16a34a;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        a:hover {
            color: #15803d;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>校园智慧信息网络中心问答助手</h1>
            <p>欢迎咨询校园网络服务相关问题</p>
        </div>
        
        <div class="main-content">
            <div class="left-panel">
                <div class="category-title">常见问题</div>
                <div class="faq-list">
                    CATEGORIES_PLACEHOLDER
                </div>
            </div>
            
            <div class="right-panel">
                <div class="chat-messages">
                    <!-- 装饰元素 -->
                    <svg class="decorator" width="120" height="120" viewBox="0 0 100 100" style="top: 60px; left: 30px; opacity: 0.07;">
                        <circle cx="50" cy="50" r="40" fill="#4CAF50"/>
                    </svg>
                    <svg class="decorator" width="100" height="100" viewBox="0 0 100 100" style="bottom: 50px; right: 60px; opacity: 0.07;">
                        <circle cx="50" cy="50" r="35" fill="#8BC34A"/>
                    </svg>
                    
                    <div class="service-info">
                        <h3>服务信息</h3>
                        SERVICE_INFO_PLACEHOLDER
                    </div>
                    
                    <div class="message bot">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            您好！我是校园智慧信息网络中心的问答助手。请问有什么可以帮助您的？
                        </div>
                        <div class="message-time">刚刚</div>
                    </div>
                    
                    FAQS_PLACEHOLDER
                </div>
                
                <div class="chat-input">
                    <input type="text" id="user-input" placeholder="请输入您的问题...">
                    <button id="send-btn">发送</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // 获取DOM元素
        const chatMessages = document.querySelector('.chat-messages');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        
        // 格式化当前时间
        function formatTime() {
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            return `${hours}:${minutes}`;
        }
        
        // 添加消息到聊天界面
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(isUser ? 'user' : 'bot');
            
            // 添加头像
            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('message-avatar');
            avatarDiv.textContent = isUser ? '👤' : '🤖';
            messageDiv.appendChild(avatarDiv);
            
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('message-content');
            
            // 检查内容是否包含特定关键词，添加动态卡片
            if (!isUser && content.includes('🏢 固定IP申请流程')) {
                // 生成随机进度值
                const progress = Math.floor(Math.random() * 70) + 30;
                const statuses = ['正在审核中', '等待部门审批', '网络配置中', '待安装设备'];
                const currentStatus = statuses[Math.floor(Math.random() * statuses.length)];
                const queueNumber = Math.floor(Math.random() * 5) + 1;
                const randomDate = new Date();
                randomDate.setDate(randomDate.getDate() + 3);
                const completionDate = randomDate.toLocaleDateString('zh-CN');
                
                // 添加动态卡片
                const cardHtml = `
                    <p>申请固定IP可按以下步骤操作 👇</p>
                    <div class="dynamic-card" onclick="toggleCard(this)">
                        <div class="card-header">
                            🏢 固定IP申请流程
                            <span class="card-arrow">▼</span>
                        </div>
                        <div class="card-content hidden">
                            <ol>
                                <li>登录<a href="https://net.scau.edu.cn" target="_blank">校园网络服务平台</a></li>
                                <li>在「服务申请」中选择「固定IP绑定」</li>
                                <li>上传设备MAC地址（格式：XX:XX:XX:XX:XX:XX）</li>
                                <li>等待24小时审核（当前排队：${queueNumber}人）</li>
                            </ol>
                            <div class="status-bar">
                                <div class="progress" style="width: ${progress}%"></div>
                                <span>今日已处理${progress}%申请</span>
                            </div>
                            <div style="margin-top: 15px; font-size: 14px; color: #4B5563; background-color: #F9FAFB; padding: 10px; border-radius: 8px;">
                                <p><strong>当前处理状态：</strong>${currentStatus}</p>
                                <p><strong>预计完成时间：</strong>${completionDate}</p>
                                <p><strong>咨询电话：</strong>8888-1234</p>
                            </div>
                        </div>
                    </div>
                `;
                contentDiv.innerHTML = cardHtml;
            } else if (!isUser && content.includes('校园网账号')) {
                // 校园网账号申请卡片
                const cardHtml = `
                    <p>校园网账号申请流程如下 👇</p>
                    <div class="dynamic-card" onclick="toggleCard(this)">
                        <div class="card-header">
                            👨‍🎓 校园网账号申请流程
                            <span class="card-arrow">▼</span>
                        </div>
                        <div class="card-content hidden">
                            <ul>
                                <li>访问信息网络中心官网：<a href="https://net.scau.edu.cn" target="_blank">net.scau.edu.cn</a></li>
                                <li>点击顶部导航栏的'账号服务'栏目</li>
                                <li>选择'校园网账号申请'选项</li>
                                <li>填写个人信息表单并上传学生证照片</li>
                                <li>提交申请后等待1-2个工作日审核</li>
                            </ul>
                            <div style="margin-top: 10px; font-size: 14px; color: #4B5563;">
                                <p><em>提示：新生入学期间可在迎新点现场办理，享受绿色通道服务。</em></p>
                            </div>
                        </div>
                    </div>
                `;
                contentDiv.innerHTML = cardHtml;
            } else {
                contentDiv.textContent = content;
            }
            
            const timeDiv = document.createElement('div');
            timeDiv.classList.add('message-time');
            timeDiv.textContent = formatTime();
            
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(timeDiv);
            
            chatMessages.appendChild(messageDiv);
            
            // 滚动到底部
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // 添加进入动画
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = isUser ? 'translateX(20px)' : 'translateX(-20px)';
            messageDiv.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                messageDiv.style.opacity = '1';
                messageDiv.style.transform = 'translateX(0)';
            }, 10);
        }
        
        // 动态展开/折叠卡片
        function toggleCard(el) {
            const content = el.querySelector('.card-content');
            const arrow = el.querySelector('.card-arrow');
            
            content.classList.toggle('hidden');
            arrow.style.transform = content.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
            
            // 展开时添加弹跳动画
            if (!content.classList.contains('hidden')) {
                content.style.animation = 'bounce 0.5s';
                
                // 重置动画以便下次点击
                setTimeout(() => {
                    content.style.animation = '';
                }, 500);
            }
        }
        
        // 发送消息
        function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;
            
            // 添加用户消息
            addMessage(message, true);
            
            // 清空输入框
            userInput.value = '';
            
            // 添加"正在输入"状态
            const typingDiv = document.createElement('div');
            typingDiv.classList.add('typing');
            typingDiv.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // 模拟AI响应延迟
            setTimeout(() => {
                // 移除"正在输入"状态
                chatMessages.removeChild(typingDiv);
                
                // 发送请求到服务器获取响应
                fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: message })
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response);
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('抱歉，暂时无法获取响应，请稍后再试。');
                });
            }, 1000);
        }
        
        // 监听发送按钮点击事件
        sendBtn.addEventListener('click', sendMessage);
        
        // 监听回车键发送消息
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // 初始化FAQ点击事件
        function initFaqEvents() {
            document.querySelectorAll('.faq-item').forEach(item => {
                item.addEventListener('click', () => {
                    const question = item.textContent.trim();
                    userInput.value = question;
                    sendMessage();
                });
            });
        }
        
        // 页面加载完成后初始化FAQ事件
        window.addEventListener('load', initFaqEvents);
        
        // 使函数全局可访问
        window.toggleCard = toggleCard;
    </script>
</body>
</html>"""
    
    # 将模板存储在全局变量中
    templates['main'] = html_template

# 渲染模板函数
def render_template(template_name, **kwargs):
    # 获取模板
    template = templates.get(template_name, '')
    
    # 处理分类占位符
    categories_html = ''
    if 'CATEGORIES_PLACEHOLDER' in template:
        # 从FAQ数据中提取所有分类
        categories = set(faq['category'] for faq in faqs)
        
        # 为每个分类生成HTML
        for category in categories:
            categories_html += f'<div class="category-title">{category}</div>'
            
            # 为该分类下的所有FAQ生成HTML
            for faq in faqs:
                if faq['category'] == category:
                    categories_html += f'<div class="faq-item">{faq["question"]}</div>'
        
        # 替换占位符
        template = template.replace('CATEGORIES_PLACEHOLDER', categories_html)
    
    # 处理FAQ占位符
    if 'FAQS_PLACEHOLDER' in template:
        # 不显示预设的FAQ消息
        template = template.replace('FAQS_PLACEHOLDER', '')
    
    # 处理服务信息占位符
    service_info_html = ''
    if 'SERVICE_INFO_PLACEHOLDER' in template:
        # 生成服务信息HTML
        service_info_html = '<ul>'
        for title, content in knowledge_base.items():
            service_info_html += f'<li><strong>{title}：</strong>{content}</li>'
        service_info_html += '</ul>'
        
        # 替换占位符
        template = template.replace('SERVICE_INFO_PLACEHOLDER', service_info_html)
    
    return template

# 自定义HTTP请求处理器
class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    # 禁用日志输出
    def log_message(self, format, *args):
        return
    
    # 处理GET请求
    def do_GET(self):
        # 处理静态文件请求
        if self.path != '/' and not self.path.startswith('/api/'):
            # 获取当前工作目录
            cwd = os.path.dirname(os.path.abspath(__file__))
            
            # 构建文件路径
            file_path = os.path.join(cwd, self.path.lstrip('/'))
            
            # 检查文件是否存在
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # 根据文件扩展名设置Content-Type
                content_type = 'application/octet-stream'
                if file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif file_path.endswith('.gif'):
                    content_type = 'image/gif'
                elif file_path.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                elif file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                
                # 设置响应头并发送文件内容
                try:
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
                except Exception as e:
                    print(f"发送文件出错: {e}")
            
            # 文件不存在或发送出错，返回404
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f"404 File not found: {self.path}".encode('utf-8'))
            return
        
        # 处理根路径请求
        if self.path == '/':
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 渲染HTML模板
            html_content = render_template('main')
            
            # 发送响应内容
            self.wfile.write(html_content.encode('utf-8'))
        else:
            # 处理404错误
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    # 处理POST请求
    def do_POST(self):
        # 处理API请求
        if self.path == '/api/query':
            # 获取请求数据长度
            content_length = int(self.headers['Content-Length'])
            
            # 读取请求数据
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_query = data.get('query', '')
                
                # 处理用户查询
                response = process_query(user_query)
                
                # 设置响应头
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # 发送响应JSON
                response_json = json.dumps({'response': response})
                self.wfile.write(response_json.encode('utf-8'))
            except Exception as e:
                # 处理错误
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = json.dumps({'error': str(e)})
                self.wfile.write(error_response.encode('utf-8'))
        else:
            # 处理404错误
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    # 处理OPTIONS请求（用于CORS）
    def do_OPTIONS(self):
        # 设置CORS响应头
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# 运行HTTP服务器的函数
def run_http_server():
    try:
        # 初始化数据
        init_data()
        
        # 创建HTTP服务器
        port = 5001
        httpd = HTTPServer(('', port), CustomHTTPRequestHandler)
        
        print(f"服务器启动成功，访问地址: http://127.0.0.1:{port}")
        httpd.serve_forever()
    except Exception as e:
        print(f"HTTP服务器运行出错: {e}")

# 异步主函数
async def main():
    # 创建并启动HTTP服务器线程
    server_thread = threading.Thread(target=run_http_server)
    server_thread.daemon = True
    server_thread.start()
    
    # 保持异步主线程运行
    try:
        while server_thread.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("服务器已停止")

# 主程序入口，适配不同的运行环境
if __name__ == '__main__':
    try:
        # 尝试以异步方式运行（适用于要求异步执行的环境）
        asyncio.run(main())
    except RuntimeError as re:
        # 如果已经在事件循环中
        print(f"检测到已有事件循环: {re}")
        # 在已经有事件循环的环境中，可以返回main函数供外部调用
        print("您可以直接调用已定义的异步main()函数")
    except ImportError:
        # 如果asyncio不可用，这在较老的Python版本中可能发生
        print("当前Python环境不支持异步功能")
        print("服务器启动中...")
        print(f"请在浏览器中访问: http://127.0.0.1:{port}")
        
        # 初始化数据
        init_data()
        
        # 使用传统方式启动HTTP服务器
        port = 5001
        httpd = HTTPServer(('', port), CustomHTTPRequestHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("服务器已停止")
            httpd.server_close()
    except Exception as e:
        # 捕获其他所有异常
        print(f"运行时出错: {e}")
        print("尝试以传统方式启动服务器...")
        print("服务器启动中...")
        print(f"请在浏览器中访问: http://127.0.0.1:{port}")
        
        # 初始化数据
        init_data()
        
        # 使用传统方式启动HTTP服务器
        port = 5001
        httpd = HTTPServer(('', port), CustomHTTPRequestHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("服务器已停止")
            httpd.server_close()
