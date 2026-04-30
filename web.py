from flask import Flask, render_template_string
import os
import markdown

app = Flask(__name__)

OUTPUT_DIR = "output"


def get_posts():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".md")]
    return [f.replace(".md", "") for f in files]


@app.route("/")
def home():
    posts = get_posts()

    html = """
    <h1>🧠 AI 内容博客</h1>
    <p>自动生成内容系统</p>
    <ul>
    """

    for p in posts:
        html += f'<li><a href="/post/{p}">{p}</a></li>'

    html += "</ul>"
    return html


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
        <title>{{title}}</title>
        <meta name="description" content="AI自动生成博客文章">
    </head>
    <body>
        <a href="/">← 返回首页</a>
        <hr>
        <div style="max-width:800px;margin:auto;">
            {{content|safe}}
        </div>
    </body>
    </html>
    """, content=html_content, title=slug)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
