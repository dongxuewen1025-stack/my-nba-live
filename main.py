import requests
import time
import re

VALID_EXTENSIONS = ('.m3u8', '.ts', '.flv', '.mp4')

def is_real_stream(url):
    url_lower = url.lower().split('?')[0]
    return any(url_lower.endswith(ext) for ext in VALID_EXTENSIONS)

def normalize_extinf(line, channel_name):
    """强制把所有频道归到同一个 group-title，方便 app 统一显示"""
    # 去掉原有 group-title
    line = re.sub(r'group-title="[^"]*"', '', line)
    # 统一注入 group-title="体育"
    line = line.replace('#EXTINF:-1', '#EXTINF:-1 group-title="体育"')
    return line

def filter_nba_channels():
    sources = [
        "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
        "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u",
        "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
        "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u",
        "https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/bestiptv.m3u",
        "https://raw.githubusercontent.com/ymyuuu/IPTVLIST/main/BestTV.m3u",
        "https://raw.githubusercontent.com/Moezx/tv/main/Taiwan.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tw.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hk.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u",
    ]

    keywords = [
        "NBA",
        "CCTV-5", "CCTV5", "CCTV 5", "5+体育", "5+體育",
        "纬来", "緯來", "Videoland",
        "爱尔达", "愛爾達", "ELTA",
        "广东体育", "廣東體育", "广体",
        "五星体育", "五星體育",
        "精品体育", "精品體育",
        "安徽体育", "安徽體育",
        "体育", "體育", "Sports",
    ]

    # 这些域名已知返回 HTML 广告页，不管后缀是什么都丢掉
    FAKE_DOMAINS = [
        "spread.3yl.xyz",
        "3yl.xyz",
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    new_m3u = ["#EXTM3U"]
    added_links = set()
    count = 0
    fake_count = 0

    for source_url in sources:
        for attempt in range(2):
            try:
                print(f"正在抓取: {source_url[:60]}...")
                r = requests.get(source_url, headers=headers, timeout=25)
                r.raise_for_status()
                r.encoding = 'utf-8'
                lines = r.text.splitlines()

                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith("#EXTINF") and any(
                        kw.upper() in line.upper() for kw in keywords
                    ):
                        for j in range(i + 1, min(i + 5, len(lines))):
                            link = lines[j].strip()
                            if link.startswith("http") and link not in added_links:
                                channel_name = line.split(",")[-1].strip()

                                # 过滤假域名
                                is_fake_domain = any(d in link for d in FAKE_DOMAINS)
                                # 过滤非流地址
                                if is_real_stream(link) and not is_fake_domain:
                                    clean_line = normalize_extinf(line, channel_name)
                                    new_m3u.append(clean_line)
                                    new_m3u.append(link)
                                    added_links.add(link)
                                    print(f"  ✅ {channel_name}  ({link[-35:]})")
                                    count += 1
                                else:
                                    print(f"  🚫 丢弃: {channel_name}")
                                    fake_count += 1
                                break
                    i += 1
                break

            except Exception as e:
                if attempt == 0:
                    print(f"  ⚠️  失败，1秒后重试... ({e})")
                    time.sleep(1)
                else:
                    print(f"  ❌ 跳过: {e}")

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))

    print(f"\n🚀 完成！真实流 {count} 个，丢弃假地址 {fake_count} 个。")

if __name__ == "__main__":
    filter_nba_channels()
