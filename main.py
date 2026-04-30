import requests
import time

def filter_nba_channels():
    sources = [
        # 综合大源
        "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
        "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u",
        "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
        "https://raw.githubusercontent.com/ymyuuu/IPTVLIST/main/BestTV.m3u",
        "https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/bestiptv.m3u",
        "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u",
        "https://raw.githubusercontent.com/xiaoz-cn/iptv/main/iptv.m3u",
        "https://raw.githubusercontent.com/loveminimal/iptv-cn/main/channels.m3u",
        # 专项台湾源
        "https://iptv-org.github.io/iptv/countries/tw.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tw.m3u",
        "https://raw.githubusercontent.com/Moezx/tv/main/Taiwan.m3u",
        # 专项中国源
        "https://iptv-org.github.io/iptv/countries/cn.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u",
        # 香港源（有时含 ELTA/纬来）
        "https://iptv-org.github.io/iptv/countries/hk.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hk.m3u",
    ]

    keywords = [
        "NBA",
        "CCTV-5", "CCTV5", "CCTV 5", "5+体育", "5+體育",
        "纬来", "緯來", "Videoland",
        "爱尔达", "愛爾達", "ELTA",
        "广东体育", "廣東體育", "广体",
        "五星体育", "五星體育",
        "体育", "體育", "Sports",
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    new_m3u = ["#EXTM3U"]
    added_links = set()
    count = 0

    for source_url in sources:
        for attempt in range(2):  # 每个源最多重试 2 次
            try:
                print(f"正在抓取: {source_url[:55]}...")
                r = requests.get(source_url, headers=headers, timeout=25)
                r.raise_for_status()
                r.encoding = 'utf-8'
                lines = r.text.splitlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    # 必须是 #EXTINF 行才处理，避免误匹配
                    if line.startswith("#EXTINF") and any(
                        kw.upper() in line.upper() for kw in keywords
                    ):
                        # 向下找第一条 http 链接
                        for j in range(i + 1, min(i + 5, len(lines))):
                            link = lines[j].strip()
                            if link.startswith("http") and link not in added_links:
                                channel_name = line.split(",")[-1].strip()
                                new_m3u.append(line)
                                new_m3u.append(link)
                                added_links.add(link)
                                print(f"  ✅ {channel_name}")
                                count += 1
                                break
                    i += 1

                break  # 成功则不重试

            except Exception as e:
                if attempt == 0:
                    print(f"  ⚠️  失败，1秒后重试... ({e})")
                    time.sleep(1)
                else:
                    print(f"  ❌ 跳过: {e}")

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))

    print(f"\n🚀 完成！共整合 {count} 个体育频道。")

if __name__ == "__main__":
    filter_nba_channels()
