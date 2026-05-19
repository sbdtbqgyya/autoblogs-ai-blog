import os
import sys
from google import genai
from google.genai import errors

class AutomatedBlogGenerator:
    def __init__(self, api_key: str = None):
        """
        初始化 Gemini 2.5 Flash 核心生成器
        """
        # 优先读取传入的 key，其次读取系统环境变量
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or "AIzaSyCwXZ4HfXN3NS74NZASqSAwxsrwGOdA9tE"
        
        if not self.api_key or self.api_key.startswith("把这里"):
            raise ValueError("错误：未检测到有效的 Google AI Studio API Key，请检查配置。")
        
        # 初始化官方原生客户端
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_post(self, topic: str, target_audience: str = "general users") -> str:
        """
        根据主题全自动生成一篇高质量、结构 scannable 的独立博客文章
        """
        # 构建防 AI 套话、注重排版结构的严苛 Prompt
        system_prompt = (
            f"You are an expert tech blogger writing for {target_audience}. "
            "Your writing style must be authentic, highly engaging, concise, and structured. "
            "Strictly avoid generic AI filler phrases like 'In this digital age', 'In conclusion', or 'Look no further'. "
            "Use Markdown format effectively: use clear headings (##, ###), bold key phrases, and bullet points to break down dense walls of text."
        )
        
        user_prompt = f"Write a comprehensive, deep-dive review and tutorial about: '{topic}'. Organize it with clear sections, actionable takeaways, and a structured layout."

        try:
            print(f"🚀 [Gemini Core] 正在通过原生接口全自动生成关于【{topic}】的文章...")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[system_prompt, user_prompt]
            )
            
            if not response.text:
                print("⚠️ [Gemini Core] 警告：模型返回内容为空。")
                return ""
                
            print("✨ [Gemini Core] 文章生成成功！")
            return response.text

        except errors.ClientError as e:
            print(f"❌ [API 错误] 访问被拒绝或找不到模型。错误代码: {e.status_code}, 详情: {e.message}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"💥 [网络或未知错误] 流水线中断: {str(e)}", file=sys.stderr)
            return ""

# ==========================================
# 自动化流水线本地集成测试入口
# ==========================================
if __name__ == "__main__":
    # 初始化
    generator = AutomatedBlogGenerator()
    
    # 模拟自动化列表派发的任务（这里可以拿你最想测评的工具当小白鼠）
    test_topic = "Detailed deep-dive review of Khan Academy and its AI tutor Khanmigo"
    
    article_content = generator.generate_post(topic=test_topic, target_audience="students, parents, and educators")
    
    if article_content:
        # 自动打印出预览，接下来你的主程序只需要把它丢进 markdown 文件保存、打上 Tailwind 标签就完活了！
        print("\n📝 ===== 自动化流水线：最终生成稿件预览 =====")
        print(article_content[:800] + "\n\n[...后面省略...]")
        print("================================================\n")