import pandas as pd
import os

# 1. 自动定位 tools.csv (就在脚本旁边)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "tools.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def batch_generate():
    if not os.path.exists(CSV_FILE):
        print(f"❌ 找不到 CSV 文件：{CSV_FILE}")
        return
    
    print(f"🚀 正在通过 CSV 批量加工：{CSV_FILE}")
    
    try:
        # 2. 读取 CSV
        df = pd.read_csv(CSV_FILE)
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        for index, row in df.iterrows():
            # 这里的 Name, Category, URL 必须对应 tools.csv 的第一行
            name = str(row['Name']).strip()
            cat = str(row['Category']).strip()
            url = str(row['URL']).strip()
            
            filename = f"{name.lower().replace(' ', '_')}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            content = (
                f"# Category: {cat}\n"
                f"# Title: {name}\n"
                f"# Link: {url}\n\n"
                f"--- \n\n"  # 加上分割线
                f"## 🚀 工具档案：{name}\n\n"
                f"> **一句话简介**：发现最前沿的 AI 生产力工具，助力创意无限可能。\n\n"
                f"| 字段 | 详细信息 |\n"
                f"| :--- | :--- |\n"
                f"| **工具名称** | {name} |\n"
                f"| **所属分类** | {cat} |\n"
                f"| **官方地址** | [点击直达官网]({url}) |\n\n"
                f"### 💡 核心亮点\n"
                f"1. **高效便捷**：针对 {cat} 领域的痛点提供专业解决方案。\n"
                f"2. **全自动入库**：本站通过自动化脚本实时更新，确保链接有效性。\n"
                f"3. **免费资源**：优先挑选高质量、易上手的免费 AI 工具。\n\n"
                f"--- \n"
                f"*注：本文由 AI 自动化流水线生成。如需深度测评，请联系站长或关注后续更新。*"
            )            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ [{index+1}] 成功生成: {filename}")
            
    except Exception as e:
        print(f"❌ 运行报错了: {e}")

if __name__ == "__main__":
    batch_generate()