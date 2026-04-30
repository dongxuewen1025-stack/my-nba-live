import requests
import time

def filter_nba_channels():
    # 换回这个源，它虽然没有海外台，但国内体育台非常全且稳定
    source_url = "https://live.fanmingming.com/tv/m3u/ipv6.m3u"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print("正在连接直播源...")
        r = requests.get(source_url, headers=headers, timeout=20)
        r.raise_for_status()
        r.encoding = 'utf-8'
    except Exception as e:
        print(f"连接失败: {e}")
        return

    lines = r.text.split('\n')
    new_m3u = ["#EXTM3U"]
    
    # 缩小范围，只找最核心的体育频道
    keywords = ["CCTV-5", "5+", "体育", "赛事", "广东体育", "五星体育", "劲爆", "NBA"]
    
    count = 0
    for i in range(len(lines)):
        line = lines[i].strip()
        # 只要这一行包含上面任何一个关键词（忽略大小写）
        if any(word.upper() in line.upper() for word in keywords):
            # 找到当前行的下一行链接
            if i + 1 < len(lines):
                link = lines[i+1].strip()
                if link.startswith("http"):
                    new_m3u.append(line)
                    new_m3u.append(link)
                    print(f"✅ 捕获成功: {line.split(',')[-1]}")
                    count += 1

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"\n🚀 任务完成！本次共抓取到 {count} 个频道。")

if __name__ == "__main__":
    filter_nba_channels()
