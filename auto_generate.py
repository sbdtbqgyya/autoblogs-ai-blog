import os
import datetime
import subprocess
from dotenv import load_dotenv

load_dotenv()
env = os.environ.copy()
env["PYTHONPATH"] = "."
os.makedirs("output", exist_ok=True)

topics = ["AI赚钱方法", "ChatGPT教程", "自动化副业", "AI工具推荐", "AI写作赚钱"]
PROMPT_TEMPLATE = "写一篇关于{topic}的SEO博客文章，适合新手阅读，结构清晰，有小标题"
KEYWORDS = "AI, ChatGPT, 自动化, 副业, 赚钱"
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
generated_files = []

print(f"🎬 自动化博客流水线启动 | 任务总数: {len(topics)} 篇")
print("==================================================")

for i, topic in enumerate(topics):
    filename = f"post-{today}-{i}.md"
    print(f"\n[任务 {i+1}/{len(topics)}] 🚀 正在生成: {filename} (主题: {topic})")
    print("-" * 50)
    
    process = subprocess.Popen(
        ["./venv/bin/python", "autoblogs/cli/main.py"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=env
    )
    
    input_data = f"{topic}\n{PROMPT_TEMPLATE.format(topic=topic)}\n{KEYWORDS}\n{filename}\n"
    stdout, stderr = process.communicate(input_data)
    
    if stdout.strip(): print(stdout)
    if stderr.strip(): print("⚠️ 阶段性反馈：", stderr)
    
    output_path = os.path.join("output", filename)
    if os.path.exists(output_path):
        print(f"✅ 成功生成文件: {output_path}")
        generated_files.append(filename)
    else:
        print(f"❌ 失败: 目录下未检测到 {filename}")

print("\n====================")
print(f"🎉 阶段生成完成！成功: {len(generated_files)} / {len(topics)} 篇")
print("====================")

if len(generated_files) == 0:
    print("❌ 没有任何文章生成成功，终止 Git 提交。")
    exit()

print("\n📦 开始打包提交到 GitHub...")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"auto batch post {today} (Success: {len(generated_files)})"])
print("📡 正在推送到远端仓库...")
push_result = subprocess.run(["git", "push"])

if push_result.returncode != 0:
    print("⚠️ push 失败，请检查网络或 GitHub Token 配置。")
else:
    print("🚀 代码及文章已成功推送至 GitHub！")

print("\n🎉 自动化内容发布系统运行完毕！")
