import os
import markdown
from flask import Flask, render_template, abort, request

app = Flask(__name__)

# 你的项目输出路径
OUTPUT_DIR = "/mnt/g/autoblogs-master/autoblogs-master/output"

def get_posts_data():
    if not os.path.exists(OUTPUT_DIR):
        return [], 0
    posts = []
    if os.path.exists(OUTPUT_DIR):
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.md')]
        for filename in files:
            posts.append({
                'title': filename.replace('.md', '').replace('_', ' '),
                'url': filename,
                'date': '2026-05-08',
                'category': 'AI 工具'
            })
    return posts, len(posts)

@app.route('/')
def home():
    all_posts, total = get_posts_data()
    return render_template("index.html", posts=all_posts, total_count=total)

@app.route('/post/<path:filename>')
def post_detail(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        html_content = markdown.markdown(content)
    return render_template("post.html", 
                         title=filename.replace('.md', '').replace('_', ' '), 
                         content=html_content, 
                         date='2026-05-08',
                         category='AI 工具')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
