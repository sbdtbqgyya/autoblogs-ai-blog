import os
import datetime
import subprocess
from dotenv import load_dotenv

# 初始化环境变量
load_dotenv()

env = os.environ.copy()
env["PYTHONPATH"] = "."

# 确保输出目录存在
os.makedirs("output", exist_ok=True)

# 待生成的主题
topics = [
    "AI赚钱方法",
    "ChatGPT教程",
    "自动化副业",
    "AI工具推荐",
    "AI写作赚钱"
]

PROMPT_TEMPLATE = "写一篇关于{topic}的SEO博客文章，适合新手阅读，结构清晰，有小标题"
KEYWORDS = "AI, ChatGPT, 自动化, 副业, 赚钱"

today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
generated_files = []

print(f"🎬 自动化博客流水线启动 | 任务总数: {len(topics)} 篇")
print("==================================================")

for i, topic in enumerate(topics):
    # 修正文件名：直接使用漂亮的中文主题作为文件名
    filename = f"{topic}.md"
    print(f"\n[任务 {i+1}/{len(topics)}] 🚀 正在生成: {filename}")
    print("-" * 50)

    # 唤醒底层的 CLI 工具
    process = subprocess.Popen(
        ["./venv/bin/python", "autoblogs/cli/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    # 严格匹配传入顺序
    input_data = f"{topic}\n{PROMPT_TEMPLATE.format(topic=topic)}\n{KEYWORDS}\n{filename}\n"

    stdout, stderr = process.communicate(input_data)

    if stdout.strip():
        print(stdout)

    if stderr.strip():
        print("⚠️ 阶段性反馈：", stderr)

    # 检查文件是否生成成功
    output_path = os.path.join("output", filename)
    if os.path.exists(output_path):
        # --------------------------------------------------
        # 🧠 核心重做：精准动态分类重写
        # --------------------------------------------------
        content_l = (topic + filename).lower()
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
        # 找到这一行，把 chatgpt, 自动化, 副业 全补进这个桶里
    elif any(x in content_l for x in ["工具", "ai", "agent", "autogpt", "chatgpt", "自动化", "副业"]): 
        category = "免费的AI工具"        else: 
            category = "其他免费资源"

        # 读取文件，把模板默认的 "#Category: 免费的AI工具" 替换为算出来的精准分类
        with open(output_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        
        # 替换首行分类声明
        fixed_content = file_content.replace("#Category: 免费的AI工具", f"#Category: {category}", 1)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        
        print(f"✅ 成功生成并分类至 [{category}]: {output_path}")
        generated_files.append(filename)
    else:
        print(f"❌ 失败: 目录下未检测到 {filename}")

# =========================
# 📊 总结与 Git 自动同步
# =========================
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