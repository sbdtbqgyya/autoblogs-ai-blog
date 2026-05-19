import pandas as pd
import os

# 路径指向 G 盘根目录
EXCEL_FILE = "/mnt/g/tools.xlsx"  
# 生成到当前目录下的 posts 文件夹
OUTPUT_DIR = "posts"    

def batch_generate():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 错误：在 {EXCEL_FILE} 找不到 Excel 文件！")
        return
    
    print(f"📂 正在读取：{EXCEL_FILE}")
    
    try:
        # 读取 Excel (确保你已经关闭了 Windows 上的 tools.xlsx)
        df = pd.read_excel(EXCEL_FILE)
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        for index, row in df.iterrows():
            name = str(row['Name']).strip()
            category = str(row['Category']).strip()
            url = str(row['URL']).strip()
            
            filename = f"{name.lower().replace(' ', '_')}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            content = (
                f"# Category: {category}\n"
                f"# Title: {name} - 免费AI工具资源指南\n"
                f"# Official_Link: {url}\n\n"
                f"### 🚀 工具简介\n"
                f"{name} 是一款属于 {category} 的 AI 工具。\n"
            )
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ [{index+1}] 成功: {filename}")
            
    except Exception as e:
        print(f"❌ 出错啦: {e}")

if __name__ == "__main__":
    batch_generate()
