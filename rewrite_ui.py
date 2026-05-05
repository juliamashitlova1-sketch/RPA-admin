import re
import os

filepath = r'c:\Users\Administrator\Desktop\api-gateway-admin\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    original_content = f.read()

# 1. Extract the Javascript
script_match = re.search(r'(<script>.*?</script>)', original_content, re.DOTALL)
js_code = script_match.group(1) if script_match else ""

# Modify JS `getProviderBadge` to fit new UI if it exists, or just ensure it exists
if "function getProviderBadge" not in js_code:
    badge_func = """
            function getProviderBadge(text) {
                var lower = (text || '').toLowerCase();
                if (lower.includes('openai') || lower.includes('gpt')) {
                    return '<span class="badge" style="background:rgba(0,229,255,0.2); color:#00B8D4;">' + text + '</span>';
                } else if (lower.includes('claude') || lower.includes('anthropic')) {
                    return '<span class="badge" style="background:rgba(67,24,255,0.15); color:var(--c-brand);">' + text + '</span>';
                } else if (lower.includes('gemini') || lower.includes('google')) {
                    return '<span class="badge" style="background:rgba(255,46,147,0.15); color:var(--c-accent-1);">' + text + '</span>';
                } else if (lower.includes('midjourney') || lower.includes('mj')) {
                    return '<span class="badge" style="background:rgba(255,171,0,0.2); color:#E65100;">' + text + '</span>';
                } else {
                    return '<span class="badge" style="background:rgba(0,0,0,0.05); color:var(--t-muted);">' + text + '</span>';
                }
            }
"""
    js_code = js_code.replace("function formatNumber(num) {", badge_func + "function formatNumber(num) {")
else:
    # Update existing getProviderBadge colors to match new palette
    js_code = re.sub(r'background:#e0f2fe; color:#0284c7;', r'background:rgba(0,229,255,0.2); color:#00B8D4;', js_code)
    js_code = re.sub(r'background:#f3e8ff; color:#9333ea;', r'background:rgba(67,24,255,0.15); color:var(--c-brand);', js_code)
    js_code = re.sub(r'background:#ccfbf1; color:#0f766e;', r'background:rgba(255,46,147,0.15); color:var(--c-accent-1);', js_code)
    js_code = re.sub(r'background:#fef08a; color:#a16207;', r'background:rgba(255,171,0,0.2); color:#E65100;', js_code)
    js_code = re.sub(r'font-weight:600;"', r'font-weight:700; font-family:var(--font-display);"', js_code)

# Ensure project poster images use the right HTML pattern in JS if there's any dynamic generation
js_code = js_code.replace('<div class="project-card-desc line-clamp-2">', '<div class="project-card-desc">')

# 2. Build New HTML Shell & CSS
new_html = """<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>API Nexus - NexGen Interface</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;700;900&display=swap');
        
        :root {
            --font-ui: "Inter", sans-serif;
            --font-display: "Outfit", sans-serif;
            
            /* High Contrast Colors */
            --c-brand: #4318FF; 
            --c-brand-light: rgba(67, 24, 255, 0.1);
            --c-accent-1: #FF2E93; 
            --c-accent-2: #00E5FF; 
            --c-accent-3: #FFAB00; 
            --c-success: #05CD99;
            --c-danger: #EE5D50;
            
            /* Text */
            --t-dark: #1B254B;
            --t-muted: #A3AED0;
            
            /* Glass */
            --glass-bg: rgba(255, 255, 255, 0.65);
            --glass-border: rgba(255, 255, 255, 0.9);
            --glass-shadow: 0 10px 40px -10px rgba(112, 144, 176, 0.2);
            
            /* Spacing */
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: var(--font-ui);
            background-color: #F4F7FE;
            color: var(--t-dark);
            height: 100vh;
            overflow: hidden;
            display: flex;
            position: relative;
        }

        /* Animated Background Mesh */
        .bg-mesh {
            position: absolute; inset: 0; z-index: -1; overflow: hidden;
            pointer-events: none;
            background: #F4F7FE;
        }
        .mesh-blob {
            position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.6;
            animation: drift 25s infinite alternate ease-in-out;
        }
        .mesh-1 { width: 600px; height: 600px; background: rgba(255, 46, 147, 0.4); top: -200px; left: -100px; animation-delay: 0s; }
        .mesh-2 { width: 700px; height: 700px; background: rgba(0, 229, 255, 0.3); bottom: -300px; right: -100px; animation-delay: -5s; }
        .mesh-3 { width: 500px; height: 500px; background: rgba(67, 24, 255, 0.3); top: 30%; left: 40%; animation-delay: -10s; }
        .mesh-4 { width: 400px; height: 400px; background: rgba(255, 171, 0, 0.2); top: 10%; right: 10%; animation-delay: -15s; }
        @keyframes drift { 0% { transform: translate(0, 0) scale(1); } 100% { transform: translate(150px, 80px) scale(1.1); } }

        /* Left Sidebar */
        .sidebar {
            width: 280px;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-right: 1px solid var(--glass-border);
            display: flex;
            flex-direction: column;
            padding: 32px 24px;
            z-index: 10;
        }
        
        .brand {
            font-family: var(--font-display); font-size: 30px; font-weight: 900;
            color: var(--t-dark); margin-bottom: 48px; padding-left: 12px;
            letter-spacing: -1px; display: flex; align-items: center; gap: 12px;
        }
        .brand span { color: var(--c-brand); }
        .brand-icon {
            width: 36px; height: 36px; border-radius: 10px;
            background: linear-gradient(135deg, var(--c-brand), var(--c-accent-1));
            display: flex; align-items: center; justify-content: center; color: white;
            box-shadow: 0 4px 12px rgba(67,24,255,0.3);
        }
        
        .nav-menu { display: flex; flex-direction: column; gap: 6px; flex: 1; }
        .nav-link {
            padding: 14px 18px; border-radius: 16px; font-size: 15px; font-weight: 600;
            color: var(--t-muted); cursor: pointer; transition: all 0.3s;
            border: none; background: transparent; text-align: left;
            display: flex; align-items: center; gap: 14px;
        }
        .nav-link:hover { color: var(--c-brand); background: rgba(255, 255, 255, 0.6); transform: translateX(4px); }
        .nav-link.nav-active { background: var(--c-brand); color: white; box-shadow: 0 8px 20px rgba(67, 24, 255, 0.3); transform: translateX(4px); }
        
        .sidebar-user {
            margin-top: auto; background: rgba(255,255,255,0.7); border: 1px solid var(--glass-border);
            padding: 16px; border-radius: 20px; display: flex; align-items: center; justify-content: space-between;
        }
        .sidebar-user-info { display: flex; align-items: center; gap: 12px; }
        .avatar { width: 44px; height: 44px; border-radius: 14px; background: linear-gradient(135deg, var(--c-accent-3), var(--c-accent-1)); display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-family: var(--font-display); font-size: 18px; box-shadow: 0 4px 10px rgba(255,46,147,0.3); }

        /* Main Content */
        .main-wrapper { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; }
        .top-header { height: 90px; padding: 0 40px; display: flex; align-items: center; justify-content: flex-end; }
        
        .search-glass {
            background: var(--glass-bg); backdrop-filter: blur(16px); border: 1px solid var(--glass-border);
            border-radius: 30px; padding: 12px 24px; display: flex; align-items: center; gap: 12px;
            width: 320px; box-shadow: var(--glass-shadow); transition: all 0.3s;
        }
        .search-glass:focus-within { box-shadow: 0 10px 40px -10px rgba(67, 24, 255, 0.3); border-color: rgba(67,24,255,0.3); }
        .search-glass input { border: none; background: transparent; outline: none; font-family: var(--font-ui); font-size: 15px; width: 100%; color: var(--t-dark); font-weight: 500; }
        .search-glass input::placeholder { color: var(--t-muted); font-weight: 400; }

        .main-content { flex: 1; overflow-y: auto; padding: 0 40px 60px; }
        .page-content { animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); max-width: 1400px; margin: 0 auto; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

        .page-header { margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end; }
        .page-title { font-family: var(--font-display); font-size: 40px; font-weight: 900; color: var(--t-dark); letter-spacing: -1.5px; line-height: 1.1; }
        .page-subtitle { font-size: 16px; color: var(--t-muted); font-weight: 500; margin-top: 8px; }

        /* Cards */
        .card {
            background: var(--glass-bg); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--glass-border); border-radius: 28px; padding: 32px;
            box-shadow: var(--glass-shadow); margin-bottom: 32px;
        }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        .card-title { font-family: var(--font-display); font-size: 24px; font-weight: 800; color: var(--t-dark); letter-spacing: -0.5px; }

        /* Stats Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 32px; }
        .stat-card {
            background: var(--glass-bg); backdrop-filter: blur(24px); border: 1px solid var(--glass-border);
            border-radius: 28px; padding: 28px; box-shadow: var(--glass-shadow);
            position: relative; overflow: hidden; display: flex; flex-direction: column; gap: 16px;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .stat-card:hover { transform: translateY(-6px); }
        .stat-card::after { content: ''; position: absolute; right: -20px; top: -20px; width: 120px; height: 120px; background: radial-gradient(circle, var(--accent-color) 0%, transparent 70%); opacity: 0.1; pointer-events: none; }
        
        .stat-header { display: flex; align-items: center; gap: 14px; font-weight: 600; color: var(--t-muted); font-size: 15px; }
        .stat-icon { width: 52px; height: 52px; border-radius: 18px; display: flex; align-items: center; justify-content: center; color: white; background: var(--accent-color); box-shadow: 0 8px 16px rgba(0,0,0,0.1); }
        .stat-icon svg { width: 26px; height: 26px; }
        .stat-value { font-family: var(--font-display); font-size: 46px; font-weight: 900; color: var(--t-dark); letter-spacing: -2px; line-height: 1; display: flex; align-items: baseline; gap: 4px; }
        .stat-currency { font-size: 24px; color: var(--t-muted); font-weight: 700; }

        .dashboard-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 32px; }

        /* Buttons */
        .btn { padding: 12px 28px; border-radius: 16px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.3s; border: none; display: inline-flex; align-items: center; justify-content: center; gap: 10px; font-family: var(--font-ui); }
        .btn-primary { background: var(--c-brand); color: white; box-shadow: 0 8px 24px rgba(67, 24, 255, 0.3); }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(67, 24, 255, 0.4); background: #3205E0; }
        .btn-outline { background: rgba(255,255,255,0.7); border: 2px solid var(--glass-border); color: var(--t-dark); backdrop-filter: blur(10px); }
        .btn-outline:hover { background: white; border-color: white; box-shadow: 0 8px 20px rgba(0,0,0,0.05); transform: translateY(-2px); }
        .btn-sm { padding: 8px 16px; font-size: 13px; border-radius: 12px; }
        .icon-btn { background: rgba(255,255,255,0.5); border: 1px solid var(--glass-border); border-radius: 12px; width: 36px; height: 36px; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; color: var(--t-muted); transition: all 0.2s; }
        .icon-btn:hover { background: white; color: var(--c-brand); box-shadow: 0 4px 12px rgba(0,0,0,0.05); transform: translateY(-2px); }

        /* Tables */
        .data-table { width: 100%; border-collapse: separate; border-spacing: 0; }
        .data-table th { padding: 18px 20px; text-align: left; font-size: 13px; font-weight: 700; color: var(--t-muted); text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid rgba(0,0,0,0.03); }
        .data-table td { padding: 20px; font-size: 15px; color: var(--t-dark); border-bottom: 1px solid rgba(0,0,0,0.03); font-weight: 500; vertical-align: middle; }
        .data-table tr:hover td { background: rgba(255,255,255,0.4); }
        .data-table tr:last-child td { border-bottom: none; }
        
        .cell-mono { font-family: var(--font-display); font-weight: 700; font-size: 16px; }
        
        /* Progress Bars */
        .progress-bar-container { height: 12px; background: rgba(0,0,0,0.04); border-radius: 12px; overflow: hidden; width: 100%; margin-top: 10px; }
        .progress-bar-fill { height: 100%; border-radius: 12px; transition: width 1s cubic-bezier(0.16, 1, 0.3, 1); }

        /* Badges */
        .badge { display: inline-flex; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 700; font-family: var(--font-display); letter-spacing: 0.5px; }
        .badge-success { background: rgba(5,205,153,0.15); color: #00A676; }
        .badge-danger { background: rgba(238,93,80,0.15); color: #D32F2F; }

        /* Project Cards */
        .project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 32px; }
        .project-card { background: var(--glass-bg); backdrop-filter: blur(24px); border: 1px solid var(--glass-border); border-radius: 32px; overflow: hidden; box-shadow: var(--glass-shadow); display: flex; flex-direction: column; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        .project-card:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 20px 50px rgba(112, 144, 176, 0.3); border-color: rgba(255,255,255,1); }
        .project-card-img { height: 200px; width: 100%; overflow: hidden; background: linear-gradient(135deg, var(--c-brand), var(--c-accent-1)); display: flex; justify-content: center; align-items: center; position: relative; }
        .project-card-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
        .project-card:hover .project-card-img img { transform: scale(1.05); }
        .project-card-placeholder { font-family: var(--font-display); font-size: 64px; font-weight: 900; color: rgba(255,255,255,0.5); }
        .project-card-body { padding: 32px; display: flex; flex-direction: column; flex: 1; }
        .project-card-title { font-family: var(--font-display); font-size: 22px; font-weight: 800; color: var(--t-dark); margin-bottom: 12px; letter-spacing: -0.5px; }
        .project-card-desc { font-size: 15px; color: var(--t-muted); margin-bottom: 24px; line-height: 1.6; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
        .project-card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 2px solid rgba(0,0,0,0.03); padding-top: 20px; }
        .project-card-count { font-size: 14px; font-weight: 700; color: var(--t-muted); font-family: var(--font-display); background: rgba(0,0,0,0.04); padding: 6px 12px; border-radius: 12px; }

        /* Specific Lists & Rows */
        .rank-item, .model-stat-row { display: flex; align-items: center; gap: 20px; padding: 20px 0; border-bottom: 2px dashed rgba(0,0,0,0.04); }
        .rank-item:last-child, .model-stat-row:last-child { border-bottom: none; }
        .ranking-rank { font-weight: 900; color: var(--t-muted); width: 32px; font-size: 20px; font-family: var(--font-display); }
        .ranking-name { font-weight: 600; color: var(--t-dark); width: 160px; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .ranking-value { font-weight: 900; color: var(--c-brand); font-family: var(--font-display); font-size: 20px;}
        
        .model-stat-header { display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 4px; }
        .model-stat-row { flex-direction: column; align-items: flex-start; gap: 4px; }
        .model-stat-pct { font-family: var(--font-display); font-weight: 900; color: var(--t-dark); font-size: 18px; }

        .hidden { display: none !important; }
        
        /* Modal */
        .modal-overlay { position: fixed; inset: 0; background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); display: none; align-items: center; justify-content: center; z-index: 999; }
        .modal-overlay.show { display: flex; }
        .modal-dialog { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(30px); border: 1px solid var(--glass-border); border-radius: 36px; padding: 48px; width: 100%; max-width: 540px; box-shadow: 0 30px 80px rgba(112,144,176,0.25); animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        @keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        .modal-title { font-family: var(--font-display); font-size: 28px; font-weight: 900; color: var(--t-dark); margin-bottom: 32px; letter-spacing: -1px; }
        .form-group { margin-bottom: 24px; }
        .form-label { display: block; font-size: 14px; font-weight: 700; color: var(--t-muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .form-input, .form-select, .form-textarea { width: 100%; padding: 16px 20px; background: rgba(255,255,255,0.7); border: 2px solid rgba(0,0,0,0.04); border-radius: 16px; font-size: 16px; outline: none; transition: all 0.3s; color: var(--t-dark); font-family: var(--font-ui); font-weight: 600; }
        .form-input:focus, .form-select:focus, .form-textarea:focus { border-color: var(--c-brand); background: white; box-shadow: 0 0 0 4px var(--c-brand-light); }
        .modal-footer { margin-top: 40px; display: flex; justify-content: flex-end; gap: 16px; }
        
        .pagination-wrapper { display: flex; justify-content: space-between; align-items: center; margin-top: 32px; padding-top: 24px; border-top: 2px solid rgba(0,0,0,0.03); }
        .page-btn { padding: 10px 20px; border-radius: 14px; border: none; background: rgba(255,255,255,0.6); font-weight: 700; cursor: pointer; color: var(--t-muted); font-size: 14px; transition: all 0.2s; }
        .page-btn:hover { background: white; color: var(--c-brand); }
        .page-btn.active { background: var(--c-brand); color: white; box-shadow: 0 8px 20px var(--c-brand-light); }
        .pagination-info { font-weight: 600; color: var(--t-muted); font-size: 14px; }
        .pagination-btns { display: flex; gap: 8px; }

        .app-footer { text-align: center; font-size: 13px; color: var(--t-muted); margin-top: 40px; padding: 24px; font-weight: 500; border-top: 1px solid rgba(0,0,0,0.05); }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <div class="bg-mesh">
        <div class="mesh-blob mesh-1"></div>
        <div class="mesh-blob mesh-2"></div>
        <div class="mesh-blob mesh-3"></div>
        <div class="mesh-blob mesh-4"></div>
    </div>

    <nav class="sidebar">
        <div class="brand">
            <div class="brand-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            API<span>Nexus</span>
        </div>
        
        <div class="nav-menu">
            <button class="nav-link nav-active" onclick="showPage('dashboard')" data-page="dashboard">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                控制面板
            </button>
            <button class="nav-link" onclick="showPage('users')" data-page="users">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                客户管理
            </button>
            <button class="nav-link" onclick="showPage('tokens')" data-page="tokens">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path></svg>
                密钥管理
            </button>
            <button class="nav-link" onclick="showPage('usage')" data-page="usage">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                流量指数
            </button>
            <button class="nav-link" onclick="showPage('pricing')" data-page="pricing">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                定价策略
            </button>
            <button class="nav-link" onclick="showPage('logs')" data-page="logs">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                系统审计
            </button>
            <button class="nav-link" onclick="showPage('projects')" data-page="projects">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                项目管理
            </button>
            <button class="nav-link" onclick="showPage('tutorials')" data-page="tutorials">
                <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                使用说明
            </button>
        </div>

        <div class="sidebar-user">
            <div class="sidebar-user-info">
                <div class="avatar">AN</div>
                <div>
                    <div style="font-weight: 800; font-family: var(--font-display); font-size: 16px; color: var(--t-dark);" id="nav-username">Admin</div>
                    <div style="font-size: 13px; font-weight: 500; color: var(--t-muted);">System Operator</div>
                </div>
            </div>
            <button class="icon-btn" onclick="logout()" title="退出系统">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            </button>
        </div>
    </nav>

    <div class="main-wrapper">
        <header class="top-header">
            <div class="search-glass">
                <svg width="20" height="20" fill="none" stroke="var(--t-muted)" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                <input type="text" placeholder="Search the nexus...">
            </div>
        </header>

        <main class="main-content">
            <!-- Dashboard -->
            <div id="page-dashboard" class="page-content">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">数据概览</h2>
                        <p class="page-subtitle">实时监控您的 API 使用情况和流量</p>
                    </div>
                    <button class="btn btn-outline" onclick="loadDashboard()">
                        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                        刷新数据
                    </button>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card" style="--accent-color: var(--c-brand);">
                        <div class="stat-header">
                            <div class="stat-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg></div>
                            今日调用量
                        </div>
                        <div class="stat-value" id="stat-calls">0</div>
                    </div>
                    <div class="stat-card" style="--accent-color: var(--c-accent-3);">
                        <div class="stat-header">
                            <div class="stat-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>
                            今日消耗
                        </div>
                        <div class="stat-value"><span class="stat-currency">¥</span><span id="stat-cost">0.00</span></div>
                    </div>
                    <div class="stat-card" style="--accent-color: var(--c-accent-1);">
                        <div class="stat-header">
                            <div class="stat-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg></div>
                            活跃用户
                        </div>
                        <div class="stat-value" id="stat-users">0</div>
                    </div>
                    <div class="stat-card" style="--accent-color: var(--c-success);">
                        <div class="stat-header">
                            <div class="stat-icon"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg></div>
                            请求成功率
                        </div>
                        <div class="stat-value" id="stat-success">0%</div>
                    </div>
                </div>

                <div class="dashboard-layout">
                    <div class="dashboard-col">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">用户消耗排名 <span style="color:var(--t-muted); font-size: 16px;">(TOP 10)</span></h3>
                            </div>
                            <div id="user-ranking">
                                <p style="color: var(--t-muted); font-weight: 500;">暂无数据</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-col">
                        <div class="card">
                            <div class="card-header">
                                <h3 class="card-title">模型调用分布</h3>
                            </div>
                            <div id="model-stats">
                                <p style="color: var(--t-muted); font-weight: 500;">暂无数据</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Users -->
            <div id="page-users" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">客户管理</h2>
                        <p class="page-subtitle">管理系统用户及其充值状态</p>
                    </div>
                    <button class="btn btn-primary" onclick="showAddUserModal()">添加新用户</button>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>用户名</th>
                                    <th>邮箱</th>
                                    <th class="text-right">余额</th>
                                    <th class="text-center">状态</th>
                                    <th>注册时间</th>
                                    <th class="text-right">操作</th>
                                </tr>
                            </thead>
                            <tbody id="users-table-body"></tbody>
                        </table>
                    </div>
                    <div id="users-pagination" class="pagination-wrapper"></div>
                </div>
            </div>

            <!-- Tokens -->
            <div id="page-tokens" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">密钥管理</h2>
                        <p class="page-subtitle">管理所有用户的 API 密钥</p>
                    </div>
                    <button class="btn btn-primary" onclick="showCreateTokenModal()">创建新Token</button>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Token名称</th>
                                    <th>Token</th>
                                    <th>所属用户</th>
                                    <th class="text-right">余额</th>
                                    <th class="text-center">状态</th>
                                    <th>创建时间</th>
                                    <th class="text-right">操作</th>
                                </tr>
                            </thead>
                            <tbody id="tokens-table-body"></tbody>
                        </table>
                    </div>
                    <div id="tokens-pagination" class="pagination-wrapper"></div>
                </div>
            </div>

            <!-- Usage -->
            <div id="page-usage" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">流量指数</h2>
                        <p class="page-subtitle">实时监控 API 请求明细</p>
                    </div>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>时间</th>
                                    <th>模型/渠道</th>
                                    <th>来源软件</th>
                                    <th class="text-right">消耗Token</th>
                                    <th class="text-right">扣费金额</th>
                                    <th class="text-center">状态</th>
                                </tr>
                            </thead>
                            <tbody id="usage-table-body"></tbody>
                        </table>
                    </div>
                    <div id="usage-pagination" class="pagination-wrapper"></div>
                </div>
            </div>

            <!-- Pricing -->
            <div id="page-pricing" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">定价策略</h2>
                        <p class="page-subtitle">管理 API 模型的计费规则</p>
                    </div>
                    <button class="btn btn-primary" onclick="showAddPricingModal()">添加定价规则</button>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>模型名称</th>
                                    <th class="text-right">输入倍率</th>
                                    <th class="text-right">输出倍率</th>
                                    <th class="text-right">单次计费(元)</th>
                                    <th class="text-center">渠道</th>
                                    <th class="text-right">操作</th>
                                </tr>
                            </thead>
                            <tbody id="pricing-table-body"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Logs -->
            <div id="page-logs" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">系统审计</h2>
                        <p class="page-subtitle">系统操作日志记录</p>
                    </div>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>时间</th>
                                    <th>操作类型</th>
                                    <th>详细信息</th>
                                </tr>
                            </thead>
                            <tbody id="logs-table-body"></tbody>
                        </table>
                    </div>
                    <div id="logs-pagination" class="pagination-wrapper"></div>
                </div>
            </div>

            <!-- Projects -->
            <div id="page-projects" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">项目管理</h2>
                        <p class="page-subtitle">管理所有项目信息与海报</p>
                    </div>
                    <button class="btn btn-primary" onclick="showAddProjectModal()">添加新项目</button>
                </div>
                <div id="projects-grid" class="project-grid"></div>
            </div>

            <!-- Tutorials -->
            <div id="page-tutorials" class="page-content hidden">
                <div class="page-header">
                    <div>
                        <h2 class="page-title">使用说明</h2>
                        <p class="page-subtitle">管理系统功能的使用教程</p>
                    </div>
                    <button class="btn btn-primary" onclick="showAddTutorialModal()">添加教程</button>
                </div>
                <div class="card">
                    <div style="overflow-x:auto;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>排序</th>
                                    <th>教程标题</th>
                                    <th>关联项目</th>
                                    <th>价格信息</th>
                                    <th class="text-right">操作</th>
                                </tr>
                            </thead>
                            <tbody id="tutorials-table-body"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <footer class="app-footer">
                © 2026 API Nexus NexGen Infrastructure. All rights reserved.
            </footer>
        </main>
    </div>

    <!-- Modals -->
    <div id="modal" class="modal-overlay">
        <div class="modal-dialog">
            <h3 id="modal-title" class="modal-title"></h3>
            <div id="modal-content"></div>
            <div class="modal-footer">
                <button class="btn btn-outline" onclick="closeModal()">取消</button>
                <button class="btn btn-primary" id="modal-confirm">确认</button>
            </div>
        </div>
    </div>

"""

final_html = new_html + js_code

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_html)
