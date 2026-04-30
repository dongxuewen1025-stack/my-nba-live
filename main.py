import requests
import time

def filter_nba_channels():
    # 两个核心源：一个稳（范明明），一个全（YueChan）
    sources = [
        "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
        "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    new_m3u = ["#EXTM3U"]
    added_links = set()
    count = 0
    
    # 覆盖简繁体、大小写的关键词
    keywords = ["NBA", "CCTV-5", "5+", "纬来", "緯來", "爱尔达", "愛爾達", "ELTA", "体育", "體育", "五星", "广东体育", "广体"]

    for source_url in sources:
        try:
            print(f"正在尝试从源抓取: {source_url[:40]}...")
            r = requests.get(source_url, headers=headers, timeout=20)
            r.raise_for_status()
            r.encoding = 'utf-8'
            
            lines = r.text.split('\n')
            for i in range(len(lines)):
                line = lines[i].strip()
                # 检查是否包含关键词
                if any(word.upper() in line.upper() for word in keywords):
                    # 向下查找最多3行找链接
                    for j in range(i + 1, min(i + 4, len(lines))):
                        link = lines[j].strip()
                        if link.startswith("http") and link not in added_links:
                            new_m3u.append(line)
                            new_m3u.append(link)
                            added_links.add(link)
                            print(f"✅ 捕获成功: {line.split(',')[-1]}")
                            count += 1
                            break
        except Exception as e:
            print(f"该源访问失败，跳过: {e}")

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"\n🚀 搜索结束！共为您整合了 {count} 个体育相关频道。")

if __name__ == "__main__":
    filter_nba_channels()
