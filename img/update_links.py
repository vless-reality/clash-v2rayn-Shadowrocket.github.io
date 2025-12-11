import re
import requests
import datetime
import pytz

# 这里存放你收集到的所有开源订阅源 (越多越好，脚本会自动筛选能用的)
# 格式: ("名称/描述", "URL", "类型: clash 或 v2ray")
SOURCES = [
    # Clash Sources
    ("ChromeGo Merge", "https://raw.githubusercontent.com/Misaka-blog/chromego_merge/main/sub/base64.txt", "clash"),
    ("Ermaozi Clash", "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml", "clash"),
    ("VPE Clash", "https://raw.githubusercontent.com/vpe/free-proxies/main/clash/provider.yaml", "clash"),
    ("Pmsub Clash", "https://sub.pmsub.me/clash.yaml", "clash"),
    ("Maoo Clash", "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/EternityAir", "clash"),
    
    # V2Ray/Base64 Sources
    ("Ermaozi V2ray", "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt", "v2ray"),
    ("FreeFQ", "https://raw.githubusercontent.com/freefq/free/master/v2", "v2ray"),
    ("Pmsub Base64", "https://sub.pmsub.me/base64", "v2ray"),
    ("Pawdroid", "https://raw.githubusercontent.com/pawdroid/Free-servers/main/sub", "v2ray"),
    ("Aiboboxx", "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2", "v2ray")
]

def check_url(url):
    """检测链接是否有效 (返回 200 OK)"""
    try:
        r = requests.head(url, timeout=5)
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

    # 构建 Markdown 文本
    content = ""
    
    # 1. 推荐部分 (默认放 ChromeGo 或第一个 Clash)
    content += "### 1. 精选推荐 (自动优选)\n"
    content += "经过自动测试连通性最好的节点池。\n"
    content += "```yaml\n"
    if valid_clash:
        content += f"{valid_clash[0]}\n"
    content += "```\n\n"

    # 2. Clash 部分
    content += "### 2. Clash 订阅链接 (.yaml)\n"
    content += "适用于 Clash for Windows, Clash Verge, ClashX, Clash for Android\n"
    content += "```yaml\n"
    for url in valid_clash: # 列出所有有效的
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

def update_readme():
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 更新日期
    tz = pytz.timezone('Asia/Shanghai')
    today = datetime.datetime.now(tz).strftime('%Y.%m.%d')
    # 正则替换日期标记之间的时间
    content = re.sub(r'<!-- DATE_START -->.*?<!-- DATE_END -->', 
                     f'<!-- DATE_START -->{today}<!-- DATE_END -->', content)

    # 2. 更新链接池
    new_links = generate_section()
    # 正则替换链接池标记之间的内容
    content = re.sub(r'<!-- LINK_POOL_START -->[\s\S]*?<!-- LINK_POOL_END -->', 
                     f'<!-- LINK_POOL_START -->\n{new_links}\n<!-- LINK_POOL_END -->', content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("README.md 更新完成！")

if __name__ == "__main__":
    update_readme()