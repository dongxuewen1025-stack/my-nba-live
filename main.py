import requests
import time

def filter_nba_channels():
    # 这个源是目前最全的，包含很多体育台
    source_url = "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print("正在连接体育大池子...")
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
    except Exception as e:
        print(f"连接失败: {e}")
        return

    lines = r.text.split('\n')
    new_m3u = ["#EXTM3U"]
    
    # 核心关键词（涵盖了所有可能播 NBA 的台）
    # 加入繁体关键词，确保万无一失
    keywords = [
        "NBA", "纬来", "緯來", "爱尔达", "愛爾達", "ELTA", 
        "体育", "體育", "五星", "广东体育", "廣東體育", "劲爆", "腾讯"
    ]
    
    added_links = set()
    count = 0

    for i in range(len(lines)):
        line = lines[i].strip()
        # 如果是描述行（包含 #EXTINF）
        if "#EXTINF" in line:
            # 检查是否包含关键词
            if any(word.upper() in line.upper() for word in keywords):
                # 寻找紧随其后的链接行
                for j in range(i + 1, min(i + 5, len(lines))):
                    link = lines[j].strip()
                    if link.startswith("http"):
                        if link not in added_links:
                            new_m3u.append(line)
                            new_m3u.append(link)
                            added_links.add(link)
                            # 在日志里打印具体名字，方便我们看
                            channel_name = line.split(',')[-1]
                            print(f"✅ 捕获成功: {channel_name}")
                            count += 1
                        break

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"\n🚀 任务完成！本次共抓取到 {count} 个体育/NBA 频道。")

if __name__ == "__main__":
    filter_nba_channels()
