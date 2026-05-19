import os
import re
import markdown
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
# 确保此路径指向你的 Markdown 文件夹
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

def get_posts_data():
    posts = []
    if not os.path.exists(OUTPUT_DIR): return posts
    url_pattern = r'https?://[^\s\)\u4e00-\u9fa5]+'
    
    # 1. 把所有合法的 .md 文件全路径抓出来
    all_files = [
        os.path.join(OUTPUT_DIR, filename)
        for filename in os.listdir(OUTPUT_DIR)
        if filename.endswith(".md")
    ]
    
    # 2. 遍历解析
    for file_path in all_files:
        filename = os.path.basename(file_path)
        file_mtime = os.path.getmtime(file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
            title = filename.replace(".md", "").replace("_", " ")
            
            # 提取官网链接
            link_match = re.search(url_pattern, raw_content)
            official_link = link_match.group(0).strip().rstrip(').,，。 ') if link_match else "#"
            
            # 🔥🔥🔥 纯手工、无盲区、绝不翻车的时间提取逻辑
            update_date = None
            lines = raw_content.splitlines()
            
            # 逐行扫描，只要哪一行包含了 updated 关键字和长得像日期的东西，直接拿走
            for line in lines:
                if "updated" in line.lower():
                    date_in_line = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                    if date_in_line:
                        update_date = date_in_line.group(1)
                        break # 找到了就立刻退出，不再往下看
            
            # 如果整篇文章里你压根就没写任何带 UPDATED 的日期行，自动用这个文件的物理修改日期保底
            if not update_date:
                update_date = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
            
            # 完好保留你最原始、绝不出错的分类判定逻辑
            raw_content_stripped = raw_content.strip()
            first_line = lines[0].strip() if lines else ""

            if first_line.replace(' ', '').startswith('#Category:'):
                category = first_line.split(':', 1)[1].strip()
            else:
                content_l = (raw_content + filename).lower()
                if any(x in content_l for x in ["亚洲", "deepseek", "kimi"]): 
                    category = "亚洲AI新星"
                elif any(x in content_l for x in ["翻译", "跨境", "monica", "immersive"]): 
                    category = "多语言跨境神器"
                elif any(x in content_l for x in ["github", "开源"]): 
                    category = "GitHub开源站"
                elif any(x in content_l for x in ["绘图", "设计", "design"]): 
                    category = "免费绘图设计"
                elif any(x in content_l for x in ["图库", "图片", "photo", "pixabay"]): 
                    category = "免费图片素材"
                elif any(x in content_l for x in ["视频", "动画", "video"]): 
                    category = "免费视频动画资源"
                elif any(x in content_l for x in ["音乐", "音频", "audio", "music", "suno"]): 
                    category = "免费AI音频音乐"
                elif any(x in content_l for x in ["教学", "课程", "学习"]): 
                    category = "免费AI教学资源"
                elif any(x in content_l for x in ["写作", "文案", "write"]): 
                    category = "免费AI写作"
                elif any(x in content_l for x in ["工具", "ai", "agent", "autogpt"]): 
                    category = "免费的AI工具"
                else: 
                    category = "其他免费资源"

            # 封装数据
            posts.append({
                "title": title, 
                "filename": filename, 
                "official_link": official_link, 
                "category_key": category,
                "date": update_date, # 极其精准的卡片日期
                "mtime": file_mtime   # 默默用于同一天内部排序的修改时间
            })
    return posts

@app.route("/")
def index():
    all_posts = get_posts_data()
    
    # 黄金组合双重排序死锁
    # 1. 优先按卡片显示的日期（date字符串，例如 2026-05-16）从大到小降序排。
    # 2. 如果显示的日期完全一样，秒看物理修改时间戳（mtime），最新保存的在最上面。
    all_posts.sort(key=lambda x: (x.get('date', ''), x.get('mtime', 0)), reverse=True)
    
    cat = request.args.get('category')
    filtered_posts = [p for p in all_posts if p['category_key'] == cat] if cat else all_posts
    return render_template("index.html", posts=filtered_posts, total_count=len(all_posts))

@app.route("/post/<filename>")
def post(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path): return "文章不存在", 404
    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()
        url_pattern = r'https?://[^\s\)\u4e00-\u9fa5]+'
        link_match = re.search(url_pattern, raw_content)
        official_link = link_match.group(0).strip().rstrip(').,，。 ') if link_match else "#"
        html_content = markdown.markdown(raw_content, extensions=['fenced_code', 'tables'])
    return render_template("post.html", title=filename.replace(".md", ""), content=html_content, official_link=official_link)

# --- PayPal 合规性页面 ---

@app.route('/privacy')
def privacy():
    return """
    <html><head><meta charset="utf-8"><title>隐私政策</title><style>
    body{font-family:sans-serif;padding:40px;background:#f8fafc;color:#334155;line-height:1.8;}
    .card{background:#fff;padding:40px;border-radius:20px;max-width:700px;margin:0 auto;box-shadow:0 4px 6px rgba(0,0,0,0.05);}
    h1{color:#0f172a;border-bottom:2px solid #3b82f6;display:inline-block;padding-bottom:10px;}
    a{color:#3b82f6;text-decoration:none;font-weight:bold;}
    </style></head><body><div class="card">
    <h1>隐私政策</h1>
    <p>本站（AI工具测评/免费资源指南）高度重视用户隐私。我们在此声明：本站仅提供资源导航与测评服务，不收集、不存储任何用户的个人隐私数据。本站不使用 Cookie 追踪个人行为。</p>
    <hr><br><a href="/">← 返回首页</a></div></body></html>
    """

@app.route('/terms')
def terms():
    return """
    <html><head><meta charset="utf-8"><title>服务条款</title><style>
    body{font-family:sans-serif;padding:40px;background:#f8fafc;color:#334155;line-height:1.8;}
    .card{background:#fff;padding:40px;border-radius:20px;max-width:700px;margin:0 auto;box-shadow:0 4px 6px rgba(0,0,0,0.05);}
    h1{color:#0f172a;border-bottom:2px solid #3b82f6;display:inline-block;padding-bottom:10px;}
    a{color:#3b82f6;text-decoration:none;font-weight:bold;}
    </style></head><body><div class="card">
    <h1>服务条款</h1>
    <p>1. 本站内容仅供学习参考。用户应自行判断第三方工具的安全性和合法性。<br>
    2. 本站不对第三方服务的变更或故障承担法律责任。<br>
    3. 访问本站即代表您同意本免责声明。</p>
    <hr><br><a href="/">← 返回首页</a></div></body></html>
    """

@app.route('/contact')
def contact():
    return """
    <html><head><meta charset="utf-8"><title>联系我们</title><style>
    body{font-family:sans-serif;padding:40px;background:#f8fafc;color:#334155;line-height:1.8;}
    .card{background:#fff;padding:40px;border-radius:20px;max-width:700px;margin:0 auto;box-shadow:0 4px 6px rgba(0,0,0,0.05);}
    h1{color:#0f172a;border-bottom:2px solid #3b82f6;display:inline-block;padding-bottom:10px;}
    a{color:#3b82f6;text-decoration:none;font-weight:bold;}
    </style></head><body><div class="card">
    <h1>联系我们</h1>
    <p>如果您有任何建议或商务需求，请通过邮件联系站长：</p>
    <p style="font-size:1.2em;background:#f1f5f9;padding:10px;border-radius:10px;display:inline-block;"><strong>sbdtbqgyy@hotmail.com</strong></p>
    <hr><br><a href="/">← 返回首页</a></div></body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)