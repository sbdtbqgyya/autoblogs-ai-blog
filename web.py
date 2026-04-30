from flask import Flask, render_template_string
import os
import markdown

app = Flask(__name__)

OUTPUT_DIR = "output"


# =========================
# 📄 获取文章列表
# =========================
def get_posts():
    if not os.path.exists(OUTPUT_DIR):
        return []

    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".md")]
    return sorted([f.replace(".md", "") for f in files], reverse=True)


# =========================
# 🏠 首页（SEO优化版）
# =========================
@app.route("/")
def home():
    posts = get_posts()

    html = """
    <html>
    <head>
        <title>AI内容博客 | 自动生成文章系统</title>
        <meta name="description" content="AI自动生成博客，涵盖ChatGPT、AI工具、自动化与生产力内容">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body style="font-family:Arial;max-width:900px;margin:auto;padding:20px;">
        <h1>🧠 AI 内容博客</h1>
        <p>自动生成内容系统（AI驱动）</p>
        <hr>
        <h2>📚 文章列表</h2>

        <ul>
    """

    if not posts:
        html += "<p>暂无文章，请先生成内容。</p>"

    for p in posts:
        html += f'<li style="margin:10px 0;"><a href="/post/{p}">📄 {p}</a></li>'

    html += """
        </ul>

        <hr>
        <p style="font-size:12px;color:gray;">
            AI Blog System • Auto Generated Content
        </p>
    </body>
    </html>
    """

    return html


# =========================
# 📄 文章页（SEO + 可扩展广告）
# =========================
@app.route("/post/<slug>")
def post(slug):
    path = os.path.join(OUTPUT_DIR, slug + ".md")

    if not os.path.exists(path):
        return "❌ 文章不存在"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    html_content = markdown.markdown(content)

    return render_template_string("""
    <html>
    <head>
        <title>{{title}} | AI博客</title>
        <meta name="description" content="AI自动生成文章：{{title}}">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body style="font-family:Arial;max-width:900px;margin:auto;padding:20px;">

        <a href="/">← 返回首页</a>

        <hr>

        <!-- 🔥 广告位（以后放 AdSense） -->
        <div style="text-align:center;margin:20px;padding:10px;border:1px dashed #ccc;">
            📢 广告位（AdSense）
        </div>

        <h1>{{title}}</h1>

        <div style="line-height:1.8;font-size:16px;">
            {{content|safe}}
        </div>

        <hr>

        <!-- 底部广告位 -->
        <div style="text-align:center;margin:20px;padding:10px;border:1px dashed #ccc;">
            📢 广告位（AdSense）
        </div>

        <p style="font-size:12px;color:gray;">
            AI Generated Article • AutoBlogs System
        </p>

    </body>
    </html>
    """, content=html_content, title=slug)


# =========================
# 🚀 启动
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)