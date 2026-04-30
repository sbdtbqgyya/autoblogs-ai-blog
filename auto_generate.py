import os
import datetime
import subprocess

# =========================
# 📅 生成文件名
# =========================
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
filename = f"post-{today}.md"

print("🚀 开始生成文章:", filename)

# =========================
# 🤖 调用 CLI（无交互版）
# =========================
env = os.environ.copy()
env["PYTHONPATH"] = "."

process = subprocess.Popen(
    ["python3", "autoblogs/cli/main.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=env
)

input_data = f"""AI工具趋势 {today}
写一篇关于AI工具、自动化和赚钱的SEO博客文章
AI工具, 自动化, ChatGPT, 赚钱, AI副业
{filename}
"""

stdout, stderr = process.communicate(input_data)

print(stdout)

if stderr:
    print("❌ 错误信息：")
    print(stderr)

# =========================
# 📂 检查是否生成成功
# =========================
output_path = os.path.join("output", filename)

if not os.path.exists(output_path):
    print("❌ 文章生成失败（未生成文件）")
    exit()

print("✅ 文章生成成功:", output_path)

# =========================
# 🚀 Git 自动提交
# =========================
os.system("git add .")
os.system(f'git commit -m "auto post {today}"')

# ⚠️ 这里不会再卡密码（前提你已设置 token）
push_result = os.system("git push")

if push_result != 0:
    print("⚠️ git push 失败（可能没设置 token）")
else:
    print("🚀 已自动推送到 GitHub")