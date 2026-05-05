import re
import os

filepath = r'c:\Users\Administrator\Desktop\api-gateway-admin\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the <style> block
new_style = """<style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            :root {
                --font-main: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                --fw-regular: 400;
                --fw-medium: 500;
                --fw-semibold: 600;
                --fw-bold: 700;
                --color-primary: #3b82f6;
                --color-primary-hover: #2563eb;
                --color-success: #10b981;
                --color-warning: #f59e0b;
                --color-danger: #ef4444;
                --color-info: #6366f1;
                --text-main: #1e293b;
                --text-secondary: #64748b;
                --text-muted: #94a3b8;
                --bg-canvas: #f0f5fa;
                --bg-card: #ffffff;
                --border-subtle: #f1f5f9;
                --border-strong: #e2e8f0;
                --border-color: #e2e8f0;
                --tag-bg-purple: #f3e8ff;
                --tag-text-purple: #9333ea;
                --tag-bg-blue: #dbeafe;
                --tag-text-blue: #2563eb;
                --tag-bg-green: #dcfce7;
                --tag-text-green: #16a34a;
                --tag-bg-red: #fee2e2;
                --tag-text-red: #dc2626;
                --radius-sm: 8px;
                --radius-md: 12px;
                --radius-lg: 16px;
                --radius-full: 9999px;
                --space-xs: 4px;
                --space-sm: 8px;
                --space-md: 12px;
                --space-lg: 20px;
                --space-xl: 24px;
                --space-2xl: 32px;
                --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
            }
            * { box-sizing: border-box; }
            body {
                background-color: var(--bg-canvas);
                font-family: var(--font-main);
                -webkit-font-smoothing: antialiased;
                color: var(--text-main);
                margin: 0;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }
            a { color: var(--color-primary); text-decoration: none; }
            a:hover { text-decoration: underline; }
            .hidden { display: none !important; }
            .pointer-events-none { pointer-events: none; }
            .aspect-video { aspect-ratio: 16 / 9; }
            .object-cover { object-fit: cover; }

            .app-wrapper {
                display: flex;
                width: 100%;
                height: 100%;
            }
            .sidebar {
                width: 68px;
                background: transparent;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: var(--space-xl) 0;
                gap: 16px;
                z-index: 10;
            }
            .sidebar-icon {
                width: 40px;
                height: 40px;
                border-radius: var(--radius-md);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s;
                background: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            .sidebar-icon:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
            
            .main-area {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .top-nav {
                height: 80px;
                padding: 0 var(--space-xl);
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-shrink: 0;
            }
            .nav-left {
                display: flex;
                align-items: center;
                gap: var(--space-xl);
            }
            .search-bar {
                background: white;
                border-radius: var(--radius-full);
                padding: 10px 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                width: 360px;
                box-shadow: var(--shadow-card);
                border: 1px solid rgba(255,255,255,0.5);
            }
            .search-bar svg { width: 16px; height: 16px; color: var(--text-muted); }
            .search-bar input {
                border: none;
                outline: none;
                width: 100%;
                font-size: 14px;
                color: var(--text-main);
                background: transparent;
            }
            .search-bar input::placeholder { color: var(--text-muted); }

            .nav-tabs {
                display: flex;
                gap: 4px;
                background: white;
                padding: 6px;
                border-radius: var(--radius-full);
                box-shadow: var(--shadow-card);
                overflow-x: auto;
            }
            .nav-link {
                padding: 8px 20px;
                border-radius: var(--radius-full);
                font-size: 14px;
                font-weight: var(--fw-medium);
                cursor: pointer;
                transition: all 0.2s;
                border: none;
                background: transparent;
                color: var(--text-secondary);
                white-space: nowrap;
            }
            .nav-link:hover { color: var(--text-main); background: var(--bg-canvas); }
            .nav-link.nav-active {
                background: var(--color-primary);
                color: white;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                font-weight: var(--fw-semibold);
            }

            .nav-right {
                display: flex;
                align-items: center;
                gap: 16px;
                background: white;
                padding: 8px 24px;
                border-radius: var(--radius-full);
                box-shadow: var(--shadow-card);
            }
            .nav-icon {
                color: var(--text-secondary);
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
            }
            .nav-icon:hover { color: var(--color-primary); }
            .nav-username { font-size: 14px; font-weight: var(--fw-semibold); color: var(--text-main); }

            .main-content {
                flex: 1;
                overflow-y: auto;
                padding: 0 var(--space-xl) var(--space-xl);
            }
            .page-content {
                max-width: 1600px;
                margin: 0 auto;
                animation: fadeIn 0.4s ease-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .page-header {
                margin-bottom: var(--space-xl);
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
            }
            .page-title {
                font-size: 24px;
                font-weight: var(--fw-bold);
                color: var(--text-main);
                letter-spacing: -0.02em;
            }
            .page-subtitle {
                font-size: 14px;
                color: var(--text-secondary);
                margin-top: 6px;
            }

            .btn {
                padding: 8px 16px;
                border-radius: var(--radius-full);
                font-size: 14px;
                font-weight: var(--fw-medium);
                cursor: pointer;
                transition: all 0.2s;
                border: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            .btn-primary { background: var(--color-primary); color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25); }
            .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35); background: var(--color-primary-hover); }
            .btn-outline { background: white; border: 1px solid var(--border-strong); color: var(--text-main); box-shadow: var(--shadow-card); }
            .btn-outline:hover { border-color: var(--color-primary); color: var(--color-primary); }
            .btn-sm { padding: 6px 12px; font-size: 12px; }

            .card {
                background: var(--bg-card);
                border-radius: var(--radius-lg);
                padding: var(--space-xl);
                margin-bottom: var(--space-xl);
                box-shadow: var(--shadow-card);
                border: 1px solid rgba(255,255,255,0.5);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .card:hover { box-shadow: var(--shadow-md); }
            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: var(--space-lg);
            }
            .card-title { font-size: 16px; font-weight: var(--fw-bold); color: var(--text-main); }
            .card-body { padding: 0; }

            .dashboard-layout {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: var(--space-xl);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: var(--space-lg);
                margin-bottom: var(--space-xl);
            }
            .stat-card {
                background: var(--bg-card);
                border-radius: var(--radius-lg);
                padding: var(--space-xl);
                box-shadow: var(--shadow-card);
                display: flex;
                flex-direction: column;
                gap: 12px;
                position: relative;
                overflow: hidden;
                border: 1px solid transparent;
                transition: all 0.2s;
            }
            .stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
            .stat-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; }
            .stat-card[data-accent="primary"]::before { background: var(--color-primary); }
            .stat-card[data-accent="info"]::before { background: var(--color-info); }
            .stat-card[data-accent="indigo"]::before { background: #8b5cf6; }
            .stat-card[data-accent="success"]::before { background: var(--color-success); }
            
            .stat-header { display: flex; align-items: center; gap: 10px; color: var(--text-secondary); font-size: 14px; font-weight: var(--fw-medium); }
            .stat-icon { width: 32px; height: 32px; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: white; }
            .stat-icon svg { width: 18px; height: 18px; }
            .stat-value-group { display: flex; align-items: baseline; gap: 4px; }
            .stat-value { font-size: 32px; font-weight: var(--fw-bold); color: var(--text-main); letter-spacing: -0.5px; }
            .stat-currency { font-size: 18px; font-weight: var(--fw-semibold); color: var(--text-secondary); }

            .data-table { width: 100%; border-collapse: separate; border-spacing: 0; }
            .data-table th { padding: 12px 16px; text-align: left; font-size: 13px; font-weight: var(--fw-semibold); color: var(--text-secondary); background: #f8fafc; border-bottom: 1px solid var(--border-subtle); }
            .data-table th:first-child { border-top-left-radius: var(--radius-sm); }
            .data-table th:last-child { border-top-right-radius: var(--radius-sm); }
            .data-table td { padding: 16px; border-bottom: 1px solid var(--border-subtle); font-size: 14px; color: var(--text-main); vertical-align: middle; }
            .data-table tr:hover td { background: #f8fafc; }
            .data-table tr:last-child td { border-bottom: none; }

            .badge { display: inline-flex; padding: 4px 12px; border-radius: var(--radius-full); font-size: 12px; font-weight: var(--fw-semibold); }
            .badge-success { background: var(--tag-bg-green); color: var(--tag-text-green); }
            .badge-danger { background: var(--tag-bg-red); color: var(--tag-text-red); }
            .badge-info { background: var(--tag-bg-blue); color: var(--tag-text-blue); }

            .progress-bar-container { width: 100%; height: 8px; background: var(--border-subtle); border-radius: var(--radius-full); overflow: hidden; margin-top: 8px;}
            .progress-bar-fill { height: 100%; border-radius: var(--radius-full); background: linear-gradient(90deg, var(--color-primary), var(--color-info)); transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1); }

            .rank-item, .model-stat-row { display: flex; align-items: center; gap: 16px; padding: 16px 0; border-bottom: 1px dashed var(--border-subtle); }
            .rank-item:last-child, .model-stat-row:last-child { border-bottom: none; }
            .ranking-rank { font-weight: var(--fw-bold); color: var(--text-muted); width: 28px; font-size: 16px; }
            .ranking-name, .model-stat-name { font-weight: var(--fw-semibold); color: var(--text-main); width: 140px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .ranking-value, .model-stat-pct { font-weight: var(--fw-bold); color: var(--color-primary); font-family: monospace; font-size: 16px;}
            
            .model-stat-header { display: flex; justify-content: space-between; width: 100%; margin-bottom: 8px; }
            .model-stat-row { flex-direction: column; align-items: flex-start; gap: 4px; }

            .modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 200; }
            .modal-overlay.show { display: flex; }
            .modal-dialog { background: var(--bg-card); border-radius: var(--radius-lg); padding: var(--space-xl); width: 100%; max-width: 480px; box-shadow: var(--shadow-md); }
            .modal-title { font-size: 18px; font-weight: var(--fw-bold); margin-bottom: 20px; }
            .modal-footer { margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px; }
            .form-group { margin-bottom: var(--space-md); }
            .form-label { display: block; font-size: 13px; font-weight: var(--fw-medium); color: var(--text-secondary); margin-bottom: 6px; }
            .form-input, .form-select, .form-textarea { width: 100%; padding: 12px 16px; border: 1px solid var(--border-strong); border-radius: var(--radius-md); font-size: 14px; font-family: inherit; transition: all 0.2s; outline: none; background: #f8fafc; }
            .form-input:focus, .form-select:focus, .form-textarea:focus { border-color: var(--color-primary); background: white; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
            
            .text-right { text-align: right; }
            .text-center { text-align: center; }
            
            .project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: var(--space-xl); }
            .project-card { background: white; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-card); transition: all 0.2s; }
            .project-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
            .project-card-img { height: 180px; background: linear-gradient(135deg, var(--color-primary), var(--color-info)); display: flex; align-items: center; justify-content: center; color: white; font-size: 28px; font-weight: bold; }
            .project-card-body { padding: var(--space-xl); }
            .project-card-title { font-size: 18px; font-weight: var(--fw-bold); margin-bottom: 8px; }
            .project-card-desc { font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.6; }
            
            .pagination-wrapper { display: flex; justify-content: space-between; align-items: center; padding-top: var(--space-lg); border-top: 1px solid var(--border-subtle); margin-top: var(--space-lg); }
            .page-btn { padding: 8px 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-strong); background: white; cursor: pointer; font-weight: var(--fw-medium); transition: all 0.2s; }
            .page-btn.active { background: var(--color-primary); color: white; border-color: var(--color-primary); box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3); }
            .pagination-info { font-size: 13px; color: var(--text-secondary); }
            .pagination-btns { display: flex; gap: 8px; }

            .app-footer {
                padding: var(--space-xl);
                color: var(--text-secondary);
                font-size: 13px;
                text-align: center;
                border-top: 1px solid var(--border-subtle);
                margin-top: auto;
            }

            @media (max-width: 1024px) {
                .dashboard-layout { grid-template-columns: 1fr; }
                .stats-grid { grid-template-columns: repeat(2, 1fr); }
            }
        </style>"""

content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

# 2. Replace the body and top nav setup
new_body_start = """    <body>
        <div class="app-wrapper">
            <!-- New Sidebar Design -->
            <aside class="sidebar">
                <div class="sidebar-icon" style="background: var(--color-info);">AN</div>
                <div class="sidebar-icon" style="background: var(--color-success);">S1</div>
                <div class="sidebar-icon" style="background: var(--color-warning);">P2</div>
                <div class="sidebar-icon" style="background: var(--color-danger);">D3</div>
                <div class="sidebar-icon" style="background: var(--tag-bg-purple); color: var(--tag-text-purple);">M4</div>
            </aside>

            <div class="main-area">
                <nav class="top-nav">
                    <div class="nav-left">
                        <div class="search-bar">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                            </svg>
                            <input type="text" placeholder="搜索模型、用户或系统记录...">
                        </div>
                    </div>
                    <div class="nav-tabs">
                        <button class="nav-link nav-active" onclick="showPage('dashboard')" data-page="dashboard">控制面板</button>
                        <button class="nav-link" onclick="showPage('users')" data-page="users">客户管理</button>
                        <button class="nav-link" onclick="showPage('tokens')" data-page="tokens">密钥管理</button>
                        <button class="nav-link" onclick="showPage('usage')" data-page="usage">流量指数</button>
                        <button class="nav-link" onclick="showPage('pricing')" data-page="pricing">定价策略</button>
                        <button class="nav-link" onclick="showPage('logs')" data-page="logs">系统审计</button>
                        <button class="nav-link" onclick="showPage('projects')" data-page="projects">项目管理</button>
                        <button class="nav-link" onclick="showPage('tutorials')" data-page="tutorials">使用说明</button>
                    </div>
                    <div class="nav-right">
                        <div class="nav-icon" title="通知">
                            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                        </div>
                        <span class="nav-username" id="nav-username">Admin</span>
                        <button class="btn btn-outline btn-sm" onclick="logout()">退出</button>
                    </div>
                </nav>
                <main class="main-content">"""

content = re.sub(r'<body>\s*<nav class="top-nav">.*?</nav>\s*<main class="main-content">', new_body_start, content, flags=re.DOTALL)

# 3. Replace the dashboard page content to use the new UI layout
new_dashboard = """            <div id="page-dashboard" class="page-content">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">数据概览</h2>
                        <p class="page-subtitle">实时监控您的 API 使用情况和流量</p>
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button class="btn btn-outline" onclick="loadDashboard()">刷新数据</button>
                    </div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card" data-accent="primary">
                        <div class="stat-header">
                            <div class="stat-icon" style="background: var(--color-primary)">
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            </div>
                            今日调用量
                        </div>
                        <div class="stat-value-group">
                            <span class="stat-value" id="stat-calls">0</span>
                        </div>
                    </div>
                    <div class="stat-card" data-accent="warning">
                        <div class="stat-header">
                            <div class="stat-icon" style="background: var(--color-warning)">
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            </div>
                            今日消耗
                        </div>
                        <div class="stat-value-group">
                            <span class="stat-currency">¥</span>
                            <span class="stat-value" id="stat-cost">0.00</span>
                        </div>
                    </div>
                    <div class="stat-card" data-accent="indigo">
                        <div class="stat-header">
                            <div class="stat-icon" style="background: #8b5cf6">
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                            </div>
                            活跃用户
                        </div>
                        <div class="stat-value-group">
                            <span class="stat-value" id="stat-users">0</span>
                        </div>
                    </div>
                    <div class="stat-card" data-accent="success">
                        <div class="stat-header">
                            <div class="stat-icon" style="background: var(--color-success)">
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                            </div>
                            请求成功率
                        </div>
                        <div class="stat-value-group">
                            <span class="stat-value" id="stat-success">0%</span>
                        </div>
                    </div>
                </div>

                <div class="dashboard-layout">
                    <!-- Left Main Column -->
                    <div class="dashboard-col">
                        <div class="card">
                            <div class="card-header" style="margin-bottom: var(--space-md);">
                                <h3 class="card-title">可用分组</h3>
                            </div>
                            <div class="nav-tabs" style="margin-bottom: var(--space-xl); display: inline-flex; box-shadow: none; border: 1px solid var(--border-subtle); padding: 4px;">
                                <button class="nav-link nav-active">全部</button>
                                <button class="nav-link">Codex</button>
                                <button class="nav-link">Claude</button>
                                <button class="nav-link">OpenAI</button>
                                <button class="nav-link">Gemini</button>
                            </div>
                            <div class="project-grid" style="grid-template-columns: repeat(2, 1fr);">
                                <div class="stat-card" style="box-shadow: none; border: 1px solid var(--border-strong);">
                                    <div style="display: flex; justify-content: space-between;">
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <span class="badge badge-info">OpenAI</span>
                                            <span style="font-weight: 600;">GPT-4-Turbo</span>
                                        </div>
                                        <span style="color: var(--color-success); font-weight: 600;">$0.01 / 1K</span>
                                    </div>
                                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 12px; margin-bottom: 8px;">
                                        支持所有 GPT-4 相关功能
                                    </div>
                                    <div class="progress-bar-container"><div class="progress-bar-fill" style="width: 85%"></div></div>
                                </div>
                                <div class="stat-card" style="box-shadow: none; border: 1px solid var(--border-strong);">
                                    <div style="display: flex; justify-content: space-between;">
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <span class="badge" style="background: var(--tag-bg-purple); color: var(--tag-text-purple);">Claude</span>
                                            <span style="font-weight: 600;">Claude-3-Opus</span>
                                        </div>
                                        <span style="color: var(--color-success); font-weight: 600;">$0.015 / 1K</span>
                                    </div>
                                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 12px; margin-bottom: 8px;">
                                        智能推理，最强语言模型
                                    </div>
                                    <div class="progress-bar-container"><div class="progress-bar-fill" style="width: 60%; background: linear-gradient(90deg, #a855f7, #6366f1)"></div></div>
                                </div>
                                <div class="stat-card" style="box-shadow: none; border: 1px solid var(--border-strong);">
                                    <div style="display: flex; justify-content: space-between;">
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <span class="badge" style="background: #e0f2fe; color: #0284c7;">Gemini</span>
                                            <span style="font-weight: 600;">Gemini-1.5-Pro</span>
                                        </div>
                                        <span style="color: var(--color-success); font-weight: 600;">$0.007 / 1K</span>
                                    </div>
                                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 12px; margin-bottom: 8px;">
                                        超大上下文，极速响应
                                    </div>
                                    <div class="progress-bar-container"><div class="progress-bar-fill" style="width: 45%; background: linear-gradient(90deg, #38bdf8, #0284c7)"></div></div>
                                </div>
                                <div class="stat-card" style="box-shadow: none; border: 1px solid var(--border-strong);">
                                    <div style="display: flex; justify-content: space-between;">
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <span class="badge" style="background: #fef08a; color: #a16207;">Midjourney</span>
                                            <span style="font-weight: 600;">MJ-V6</span>
                                        </div>
                                        <span style="color: var(--color-success); font-weight: 600;">$0.05 / 1次</span>
                                    </div>
                                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 12px; margin-bottom: 8px;">
                                        AI 绘画，无损渲染
                                    </div>
                                    <div class="progress-bar-container"><div class="progress-bar-fill" style="width: 90%; background: linear-gradient(90deg, #facc15, #ca8a04)"></div></div>
                                </div>
                            </div>
                        </div>

                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">用户消耗排名 (TOP 10)</h3>
                            </div>
                            <div class="card-body" id="user-ranking">
                                <p style="color: var(--text-muted); font-size: 14px;">暂无数据</p>
                            </div>
                        </div>
                    </div>

                    <!-- Right Stats Column -->
                    <div class="dashboard-col">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">模型调用分布</h3>
                            </div>
                            <div class="card-body" id="model-stats">
                                <p style="color: var(--text-muted); font-size: 14px;">暂无数据</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>"""

content = re.sub(r'<div id="page-dashboard" class="page-content">.*?<!-- Users -->', new_dashboard + "\n\n            <!-- Users -->", content, flags=re.DOTALL)

# 4. Fix closing tags for app-wrapper and main-area
content = re.sub(r'<footer class="app-footer">.*?</footer>\s*</main>', r'<footer class="app-footer">© 2026 API Nexus Infrastructure. Build 2.0.0</footer>\n                </main>\n            </div>\n        </div>', content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
