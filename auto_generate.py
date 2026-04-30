import os
import datetime
import subprocess
from dotenv import load_dotenv

# =========================
# 🔧 初始化
# =========================
load_dotenv()

env = os.environ.copy()
env["PYTHONPATH"] = "."

# =========================
# 🧠 可自定义内容（核心）
# =========================
topics = [
    "AI赚钱方法",
    "ChatGPT教程",
    "自动化副业",
    "AI工具推荐",
    "AI写作赚钱"
]

PROMPT_TEMPLATE = "写一篇关于{topic}的SEO博客文章，适合新手阅读，结构清晰，有小标题"
KEYWORDS = "AI, ChatGPT, 自动化, 副业, 赚钱"

# =========================
# 📅 时间
# =========================
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

# =========================
# 🚀 批量生成
# =========================
generated_files = []

for i, topic in enumerate(topics):
    filename = f"post-{today}-{i}.md"

    print(f"\n🚀 正在生成: {filename}")

    process = subprocess.Popen(
        ["./venv/bin/python", "autoblogs/cli/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    input_data = f"""{topic}
{PROMPT_TEMPLATE.format(topic=topic)}
{KEYWORDS}
{filename}
"""

    stdout, stderr = process.communicate(input_data)

    print(stdout)

    if stderr:
        print("❌ 错误：", stderr)

    # 检查文件是否生成
    output_path = os.path.join("output", filename)
    if os.path.exists(output_path):
        print(f"✅ 成功: {filename}")
        generated_files.append(filename)
    else:
        print(f"❌ 失败: {filename}")

# =========================
# 📊 总结
# =========================
print("\n====================")
print(f"生成成功: {len(generated_files)} 篇")
print("====================")

if len(generated_files) == 0:
    print("❌ 没有生成任何文章，终止")
    exit()

# =========================
# 🚀 Git 自动提交
# =========================
print("\n🚀 开始提交到 GitHub...")

os.system("git add .")
os.system(f'git commit -m "auto batch post {today}"')

push_result = os.system("git push")

if push_result != 0:
    print("⚠️ push 失败（检查 token）")
else:
    print("🚀 推送成功")

print("\n🎉 自动内容系统运行完成")