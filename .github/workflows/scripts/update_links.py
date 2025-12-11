import re
import requests
import datetime
import pytz
import os  # <--- 1. 新增：引入 os 模块

# ... (中间的 SOURCES 列表和 check_url, generate_section 函数保持不变，不需要改) ...

# ---------------------------------------------------------
# 为了节省篇幅，这里省略了中间的代码，请保留你原来的 SOURCES 等内容
# 直接跳到下面 update_readme 函数进行修改
# ---------------------------------------------------------

def update_readme():
    # <--- 2. 修改开始：智能获取 README.md 的路径 --->
    
    # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 这里的逻辑是：不管脚本藏在多深的文件夹里，我们都向上一层层找，直到找到 README.md
    # 你的路径看起来是 .github/workflows/scripts/ (三层深) 或者 .github/scripts/ (两层深)
    
    # 先尝试向上回退 2 层 (.github/scripts/)
    readme_path = os.path.abspath(os.path.join(script_dir, "..", "..", "README.md"))
    
    # 如果找不到，尝试向上回退 3 层 (兼容你报错信息里的 .github/workflows/scripts/)
    if not os.path.exists(readme_path):
        readme_path = os.path.abspath(os.path.join(script_dir, "..", "..", "..", "README.md"))
        
    print(f"正在读取文件: {readme_path}")
    
    # <--- 修改结束 --->

    if not os.path.exists(readme_path):
        print("❌ 错误：找不到 README.md 文件，请检查脚本位置！")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 更新日期
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.datetime.now(tz).strftime('%Y.%m.%d')
    content = re.sub(r'<!-- DATE_START -->.*?<!-- DATE_END -->', 
                     f'<!-- DATE_START -->{today}<!-- DATE_END -->', content)

    # 2. 更新链接池
    new_links = generate_section() # 这里调用你上面定义的函数
    content = re.sub(r'<!-- LINK_POOL_START -->[\s\S]*?<!-- LINK_POOL_END -->', 
                     f'<!-- LINK_POOL_START -->\n{new_links}\n<!-- LINK_POOL_END -->', content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("README.md 更新完成！")

if __name__ == "__main__":
    update_readme()