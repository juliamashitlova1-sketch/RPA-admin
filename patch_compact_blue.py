import re

filepath = r'c:\Users\Administrator\Desktop\api-gateway-admin\dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Mesh Background Colors to Warm Blues
content = re.sub(r'\.mesh-1 \{[^\}]+\}', r'.mesh-1 { width: 600px; height: 600px; background: rgba(74, 144, 226, 0.4); top: -200px; left: -100px; animation-delay: 0s; }', content)
content = re.sub(r'\.mesh-2 \{[^\}]+\}', r'.mesh-2 { width: 700px; height: 700px; background: rgba(92, 107, 192, 0.3); bottom: -300px; right: -100px; animation-delay: -5s; }', content)
content = re.sub(r'\.mesh-3 \{[^\}]+\}', r'.mesh-3 { width: 500px; height: 500px; background: rgba(41, 182, 246, 0.3); top: 30%; left: 40%; animation-delay: -10s; }', content)
content = re.sub(r'\.mesh-4 \{[^\}]+\}', r'.mesh-4 { width: 400px; height: 400px; background: rgba(144, 202, 249, 0.4); top: 10%; right: 10%; animation-delay: -15s; }', content)

# 2. Compact Sidebar
content = content.replace('width: 280px;', 'width: 220px;')
content = content.replace('padding: 32px 24px;', 'padding: 24px 16px;')
content = content.replace('font-size: 30px;', 'font-size: 22px;') # brand
content = content.replace('margin-bottom: 48px;', 'margin-bottom: 24px;') # brand
content = content.replace('padding: 14px 18px;', 'padding: 10px 14px;') # nav-link
content = content.replace('font-size: 15px;', 'font-size: 13px;') # nav-link / btn / table / form
content = content.replace('gap: 14px;', 'gap: 10px;') # nav-link
content = content.replace('width: 44px; height: 44px; border-radius: 14px;', 'width: 36px; height: 36px; border-radius: 10px;') # avatar
content = content.replace('font-size: 18px;', 'font-size: 15px;') # avatar font / card-title
content = content.replace('font-size: 16px;', 'font-size: 14px;') # username / table / page-subtitle

# 3. Compact Main Layout
content = content.replace('height: 90px;', 'height: 60px;') # top-header
content = content.replace('padding: 0 40px;', 'padding: 0 24px;') # top-header
content = content.replace('padding: 0 40px 60px;', 'padding: 0 24px 30px;') # main-content
content = content.replace('margin-bottom: 32px;', 'margin-bottom: 20px;') # page-header / card
content = content.replace('font-size: 40px;', 'font-size: 26px;') # page-title
content = content.replace('margin-top: 8px;', 'margin-top: 4px;') # page-subtitle

# 4. Compact Cards
content = content.replace('border-radius: 28px;', 'border-radius: 16px;') # card / stat-card
content = content.replace('padding: 32px;', 'padding: 20px;') # card
content = content.replace('margin-bottom: 24px;', 'margin-bottom: 16px;') # card-header
content = content.replace('font-size: 24px;', 'font-size: 18px;') # card-title / stat-currency
content = content.replace('padding: 28px;', 'padding: 16px;') # stat-card
content = content.replace('gap: 16px;', 'gap: 10px;') # stat-card
content = content.replace('gap: 24px;', 'gap: 16px;') # stats-grid
content = content.replace('gap: 32px;', 'gap: 20px;') # dashboard-layout / project-grid
content = content.replace('width: 52px; height: 52px; border-radius: 18px;', 'width: 36px; height: 36px; border-radius: 10px;') # stat-icon
content = content.replace('width: 26px; height: 26px;', 'width: 18px; height: 18px;') # stat-icon svg
content = content.replace('font-size: 46px;', 'font-size: 32px;') # stat-value

# 5. Compact Buttons & Inputs
content = content.replace('padding: 12px 28px;', 'padding: 8px 16px;') # btn
content = content.replace('padding: 16px 20px;', 'padding: 10px 14px;') # form-input
content = content.replace('border-radius: 16px;', 'border-radius: 10px;') # btn / form-input
content = content.replace('padding: 12px 24px;', 'padding: 8px 16px;') # search-glass
content = content.replace('border-radius: 30px;', 'border-radius: 20px;') # search-glass

# 6. Compact Tables
content = content.replace('padding: 18px 20px;', 'padding: 12px 16px;') # th
content = content.replace('padding: 20px;', 'padding: 14px 16px;') # td
content = content.replace('font-size: 13px;', 'font-size: 12px;') # th
content = content.replace('padding: 6px 14px;', 'padding: 4px 10px;') # badge

# 7. Compact Projects
content = content.replace('border-radius: 32px;', 'border-radius: 16px;') # project-card
content = content.replace('height: 200px;', 'height: 140px;') # project-card-img
content = content.replace('font-size: 22px;', 'font-size: 16px;') # project-card-title
content = content.replace('font-size: 64px;', 'font-size: 48px;') # project-card-placeholder

# Final adjustments that might have been overwritten
content = re.sub(r'font-size:\s*15px;\s*color:\s*var\(--t-dark\);\s*border-bottom:\s*1px solid', r'font-size: 13px; color: var(--t-dark); border-bottom: 1px solid', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
