import re

filepath = r'c:\Users\Administrator\Desktop\api-gateway-admin\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Compact Layout (CSS Variables)
old_spacing = """                --space-xs: 4px;
                --space-sm: 8px;
                --space-md: 10px;
                --space-lg: 16px;
                --space-xl: 20px;
                --space-2xl: 24px;"""
new_spacing = """                --space-xs: 2px;
                --space-sm: 6px;
                --space-md: 8px;
                --space-lg: 12px;
                --space-xl: 16px;
                --space-2xl: 20px;"""
content = content.replace(old_spacing, new_spacing)

# Font sizes and padding reductions
content = content.replace("font-size: 24px;", "font-size: 20px;") # page-title
content = content.replace("font-size: 32px;", "font-size: 24px;") # stat-value
content = content.replace("font-size: 16px;", "font-size: 14px;") # card-title, ranking-value
content = content.replace("padding: 12px 16px;", "padding: 8px 12px;") # data-table th
content = content.replace("padding: 16px;", "padding: 12px;") # data-table td

# 2. Add Badge Utility Function
badge_script = """            function getProviderBadge(text) {
                var lower = (text || '').toLowerCase();
                if (lower.includes('openai') || lower.includes('gpt')) {
                    return '<span class="badge" style="background:#e0f2fe; color:#0284c7; padding:2px 8px; font-size:12px; font-weight:600;">' + text + '</span>';
                } else if (lower.includes('claude') || lower.includes('anthropic')) {
                    return '<span class="badge" style="background:#f3e8ff; color:#9333ea; padding:2px 8px; font-size:12px; font-weight:600;">' + text + '</span>';
                } else if (lower.includes('gemini') || lower.includes('google')) {
                    return '<span class="badge" style="background:#ccfbf1; color:#0f766e; padding:2px 8px; font-size:12px; font-weight:600;">' + text + '</span>';
                } else if (lower.includes('midjourney') || lower.includes('mj')) {
                    return '<span class="badge" style="background:#fef08a; color:#a16207; padding:2px 8px; font-size:12px; font-weight:600;">' + text + '</span>';
                } else {
                    return '<span class="badge" style="background:var(--bg-canvas); color:var(--text-secondary); padding:2px 8px; font-size:12px; font-weight:600;">' + text + '</span>';
                }
            }"""

if "function getProviderBadge" not in content:
    content = content.replace("function formatNumber(num) {", badge_script + "\n            function formatNumber(num) {")

# 3. Replace loadUsageDetail badge
old_usage_row = """'</span></td><td><span class="badge badge-info">' +
                            r.api_provider +
                            "/" +
                            r.model +
                            '</span></td><td><span style="font-size:13px;color:var(--text-secondary)">'"""
new_usage_row = """'</span></td><td>' +
                            getProviderBadge(r.api_provider) + ' <span style="font-size:12px;color:var(--text-main);font-weight:500;">' +
                            r.model +
                            '</span></td><td><span style="font-size:13px;color:var(--text-secondary)">'"""
content = content.replace(old_usage_row, new_usage_row)

# One more variation just in case python formatting differs
content = re.sub(r'\'</span></td><td><span class="badge badge-info">\' \+\s*r.api_provider \+\s*"/" \+\s*r.model \+\s*\'</span></td><td><span style="font-size:13px;color:var\(--text-secondary\)">\'', 
                 r'\'</span></td><td>\' + getProviderBadge(r.api_provider) + \' <span style="font-size:12px;color:var(--text-main);font-weight:500;">\' + r.model + \'</span></td><td><span style="font-size:13px;color:var(--text-secondary)">\'', content)

# 4. Replace Dashboard top models distribution list to use provider badges
# In loadDashboard, there's `result.data.modelStats.map(...)`
old_model_stat = """                                    '<div class="model-stat-row"><div class="model-stat-header"><span class="model-stat-name">' +
                                    s.model +
                                    '</span><span class="model-stat-pct">' +"""
new_model_stat = """                                    '<div class="model-stat-row"><div class="model-stat-header"><span class="model-stat-name" style="display:flex;align-items:center;gap:6px;">' +
                                    getProviderBadge(s.model.split('-')[0]) + ' ' + s.model +
                                    '</span><span class="model-stat-pct">' +"""
content = content.replace(old_model_stat, new_model_stat)

content = re.sub(r'\'<div class="model-stat-row"><div class="model-stat-header"><span class="model-stat-name">\' \+\s*s.model \+\s*\'</span><span class="model-stat-pct">\' \+',
                 r'\'<div class="model-stat-row"><div class="model-stat-header"><span class="model-stat-name" style="display:flex;align-items:center;gap:6px;">\' + getProviderBadge(s.model.split("-")[0] || s.model) + \' <span style="font-size:13px;">\' + s.model + \'</span></span><span class="model-stat-pct">\' +', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
