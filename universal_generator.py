import pandas as pd
import os

# --- 关键修改：直接定位到 G 盘根目录下的文件 ---
# 在 WSL 中，G 盘的根目录路径是 /mnt/g/
EXCEL_FILE = "/mnt/g/tools.xlsx"  
OUTPUT_DIR = "posts"    # 建议直接生成到 posts 文件夹

def batch_generate():
    # 1. 检查文件是否存在
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 错误：在 {EXCEL_FILE} 找不到 Excel 文件！")
        print("请检查文件名是否准确为 tools.xlsx，且确实在 G 盘根目录。")
        return
    
    print(f"📂 正在读取数据源：{EXCEL_FILE}")
    
    try:
        # 读取 Excel
        df = pd.read_excel(EXCEL_FILE)
        
        # 2. 检查输出目录
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # 3. 循环处理
        for index, row in df.iterrows():
            # 这里的列名必须和你的 Excel 表头一模一样（Name, Category, URL）
            name = str(row['Name']).strip()
            category = str(row['Category']).strip()
            url = str(row['URL']).strip()
            
            # 格式化文件名
            safe_name = name.lower().replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # 构建博文内容（完全符合你之前的标准）
            content = (
                f"# Category: {category}\n"
                f"# Title: {name} - 免费AI工具资源指南\n"
                f"# Official_Link: {url}\n\n"
                f"### 🚀 工具简介\n"
                f"{name} 是一款非常强大的 AI 工具，属于 {category} 类别。\n\n"
                f"### 💡 核心亮点\n"
                f"* 官方原版链接保证\n"
                f"* 经过初步测评，性能稳定\n"
            )
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ [{index+1}] 成功生成: {filename}")
            
    except Exception as e:
        print(f"❌ 运行出错了：{e}")

if __name__ == "__main__":
    batch_generate()
