import os
import datetime
import subprocess

# 生成文件名（避免重复）
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
filename = f"post-{today}.md"

print("🚀 开始生成文章:", filename)

# 自动输入 CLI（模拟人工输入）
cmd = f"""
echo "AI工具趋势 {today}" | \
python3 autoblogs/cli/main.py <<EOF
AI工具趋势 {today}
写一篇关于AI工具、自动化和赚钱的SEO博客文章
AI工具, 自动化, ChatGPT, 赚钱, AI副业
{filename}
EOF
"""

os.system(cmd)

print("✅ 文章生成完成")

# =====================
# 自动 git 提交
# =====================
os.system("git add .")
os.system(f'git commit -m "auto post {today}"')
os.system("git push")

print("🚀 已自动推送到 GitHub")