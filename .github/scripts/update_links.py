import re
import requests
import datetime
import pytz
import os
import random  # <--- 1. 引入随机模块

# --------------------------------------------------------------------------------
# 1. 配置部分：这里存放所有的开源订阅源
# --------------------------------------------------------------------------------
SOURCES = [
    # Clash 订阅源
    ("ChromeGo Merge", "https://raw.githubusercontent.com/vless-reality/clash-v2rayn-Shadowrocket/refs/heads/main/.github/links/clash.yaml", "clash")
    
    # V2Ray/Base64 订阅源
    ("Ermaozi V2ray", "https://raw.githubusercontent.com/vless-reality/clash-v2rayn-Shadowrocket/refs/heads/main/.github/links/v2.txt", "v2rayn通用")

]

# --------------------------------------------------------------------------------
# 2. 功能函数部分
# --------------------------------------------------------------------------------
def check_url(url):
    """检测链接是否有效 (返回 200 OK)"""
    try:
        # 设置超时时间为 10 秒，避免卡死
        r = requests.head(url, timeout=10)
        return r.status_code == 200
    except:
        return False

def generate_section():
    """生成 Markdown 内容"""
    valid_clash = []
    valid_v2ray = []

    print("开始检测链接连通性...")
    for name, url, type_ in SOURCES:
        if check_url(url):
            print(f"✅ 有效: {name}")
            if type_ == "clash":
                valid_clash.append(url)
            else:
                valid_v2ray.append(url)
        else:
            print(f"❌ 失效: {name}")

    # ----------------------------------------------------------------
    # 核心修改：在此处打乱列表顺序
    # 这样每次生成的文件内容都不一样，Git 就能检测到变动了
    # ----------------------------------------------------------------
    if valid_clash:
        random.shuffle(valid_clash)
        print(f"🎲 已随机打乱 Clash 链接顺序 (共 {len(valid_clash)} 个)")
    
    if valid_v2ray:
        random.shuffle(valid_v2ray)
        print(f"🎲 已随机打乱 V2Ray 链接顺序 (共 {len(valid_v2ray)} 个)")
    # ----------------------------------------------------------------

    # 构建 Markdown 文本
    content = ""
    
    # 1. 推荐部分 (因为上面shuffle过，这里取第0个已经是随机的了)
    content += "### 1. ChromeGo_Merge (自动优选推荐)\n"
    content += "目前维护最勤快的节点池之一，由志愿者维护。\n"
    content += "```yaml\n"
    if valid_clash:
        content += f"{valid_clash[0]}\n"
    elif valid_v2ray: # 如果没有clash，用v2ray顶替
         content += f"{valid_v2ray[0]}\n"
    content += "```\n\n"

    # 2. Clash 部分
    content += "### 2. Clash 订阅链接 (.yaml)\n"
    content += "适用于 Clash for Windows, Clash Verge, ClashX, Clash for Android\n"
    content += "```yaml\n"
    for url in valid_clash:
        content += f"{url}\n"
    content += "```\n\n"

    # 3. V2Ray 部分
    content += "### 3. V2Ray/SSR 订阅链接 (Base64)\n"
    content += "适用于 v2rayN, Shadowrocket, QuantumultX\n"
    content += "```text\n"
    for url in valid_v2ray:
        content += f"{url}\n"
    content += "```\n"

    return content

# --------------------------------------------------------------------------------
# 3. 主逻辑部分
# --------------------------------------------------------------------------------
def update_readme():
    # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 自动寻找 README.md (向上找两层)
    readme_path = os.path.abspath(os.path.join(script_dir, "..", "..", "README.md"))
    
    # 如果找不到，尝试向上回退 3 层 (兼容 workflows 目录结构)
    if not os.path.exists(readme_path):
        readme_path = os.path.abspath(os.path.join(script_dir, "..", "..", "..", "README.md"))
        
    print(f"正在读取文件: {readme_path}")

    if not os.path.exists(readme_path):
        print("❌ 错误：找不到 README.md 文件，请检查脚本位置！")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 更新日期
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.datetime.now(tz).strftime('%Y.%m.%d')
    content = re.sub(r'<!-- DATE_START -->.*?<!-- DATE_END -->', 
                     f'<!-- DATE_START -->{today}<!-- DATE_END -->', content)

    # 更新链接池
    try:
        new_links = generate_section() 
        content = re.sub(r'<!-- LINK_POOL_START -->[\s\S]*?<!-- LINK_POOL_END -->', 
                        f'<!-- LINK_POOL_START -->\n{new_links}\n<!-- LINK_POOL_END -->', content)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md 更新完成！")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    update_readme()
