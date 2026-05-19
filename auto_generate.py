import os
import datetime
import subprocess
from dotenv import load_dotenv

# 1. 强制加载你的原生配置
load_dotenv()

env = os.environ.copy()
env["PYTHONPATH"] = "."

# 从环境变量中读取输出目录，如果没有则默认为 output
output_dir = os.getenv("CONTENT_OUTPUT_DIR", "output")
os.makedirs(output_dir, exist_ok=True)

# 🚀 你的 5 个真·内容选题
topics = [
    "DeepSeek-V3 深度测评：国产大模型性能怪兽究竟有多强？",
    "Cursor AI 编程编译器全指引：零基础如何用 AI 独立开发应用",
    "Kimi AI 超长文本分析实战：如何 10 秒提取万字财报核心数据",
    "Suno V3 自动化搞钱流：AI 音乐创作到商业变现的全套玩法",
    "Monica AI 跨境办公神器：多语言自动化翻译与工作流构建"
]

# 严格使用系统现有的 prompt 模板和关键词
PROMPT_TEMPLATE = "写一篇关于{topic}的SEO博客文章，适合新手阅读，结构清晰，有小标题"
KEYWORDS = "AI, ChatGPT, 自动化, 副业, 赚钱"
today = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

generated_files = []
print(f"🎬 系统原生大模型发布流水线启动 | 任务总数: {len(topics)} 篇")
print("==================================================")

for i, topic in enumerate(topics):
    # 用主题的主名字作为漂亮的中文文件名
    clean_title = topic.split("：")[0].strip()
    filename = f"{clean_title}.md"
    
    print(f"\n[任务 {i+1}/{len(topics)}] 🚀 正在通过底层引擎生成: {filename}")
    print("-" * 50)

    # 2. 唤醒底层的 CLI 工具，它会自动读取你给的 OpenAI 兼容端点去请求大模型
    process = subprocess.Popen(
        ["./venv/bin/python", "autoblogs/cli/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    # 3. 严格匹配你系统底层的输入流管道顺序
    input_data = f"{topic}\n{PROMPT_TEMPLATE.format(topic=topic)}\n{KEYWORDS}\n{filename}\n"
    stdout, stderr = process.communicate(input_data)

    if stdout.strip():
        print(stdout)
    if stderr.strip():
        print("⚠️ 阶段反馈：", stderr)

    # 4. 后处理：等底层大模型吐完内容后，Python 动态修正分类头部
    output_path = os.path.join(output_dir, filename)
    if os.path.exists(output_path):
        content_l = (topic + filename).lower()
        
        # 你的 11 个精准分类映射
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
        elif any(x in content_l for x in ["工具", "ai", "agent", "autogpt", "chatgpt", "自动化", "副业"]): 
            category = "免费的AI工具"
        else: 
            category = "其他免费资源"

        # 重新读取生成的真干货文件，干掉死模板里的硬编码分类，替换为刚刚算出来的精准分类
        with open(output_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        
        fixed_content = file_content.replace("#Category: 免费的AI工具", f"#Category: {category}", 1)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)
        
        print(f"✅ 深度真内容已落盘并成功分类至 [{category}]: {output_path}")
        generated_files.append(filename)
    else:
        print(f"❌ 失败: 底层未检测到生成文件 {filename}")

# =========================
# 📊 Git 自动同步真内容
# =========================
print("\n====================")
print(f"🎉 阶段生成完成！成功: {len(generated_files)} / {len(topics)} 篇")
print("====================")

if len(generated_files) == 0:
    print("❌ 没有任何文章生成成功，终止 Git 提交。")
    exit()

print("\n📦 开始打包提交到 GitHub...")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"feat: 基于原生LLM引擎自动化批量生成 {len(generated_files)} 篇深度干货"])

print("📡 正在推送到远端仓库...")
push_result = subprocess.run(["git", "push"])

if push_result.returncode != 0:
    print("⚠️ push 失败，请检查网络。")
else:
    print("🚀 真正的 AI 深度干货文章已成功同步发布至线上网站！")