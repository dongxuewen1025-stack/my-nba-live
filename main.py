import requests
import time

def filter_nba_channels():
    # 切换到一个体育频道更全的源
    source_url = "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        print("正在抓取体育源...")
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
    except Exception as e:
        print(f"抓取失败: {e}")
        return

    lines = r.text.split('\n')
    new_m3u = ["#EXTM3U"]
    
    # 针对 NBA 的精准关键词
    # 纬来和爱尔达是看 NBA 的神台，五星和广东体育偶尔有转播
    keywords = ["NBA", "纬来", "爱尔达", "ELTA", "体育", "五星", "广东体育", "劲爆体育"]
    
    added_links = set() # 用来去重，防止同一个台出现好几次
    count = 0

    for i in range(len(lines)):
        line = lines[i].strip()
        if any(word.upper() in line.upper() for word in keywords):
            if i + 1 < len(lines):
                link = lines[i+1].strip()
                if link.startswith("http") and link not in added_links:
                    new_m3u.append(line)
                    new_m3u.append(link)
                    added_links.add(link)
                    print(f"已捕获 NBA 相关频道: {line.split(',')[-1]}")
                    count += 1

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"\n🎉 搞定！为您找到了 {count} 个 NBA 可能播出的频道。")

if __name__ == "__main__":
    filter_nba_channels()
