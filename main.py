import requests
import re

def filter_sports_channels():
    # 使用社区维护的源（包含了大量 CCTV 和省级频道）
    source_url = "https://ghproxy.net/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
    
    try:
        r = requests.get(source_url, timeout=10)
        r.raise_for_status()
        lines = r.text.split('\n')
        
        new_m3u = ["#EXTM3U"]
        
        # 遍历每一行，寻找关键词
        for i in range(len(lines)):
            # 这里你可以自定义关键词，比如想要“NBA”、“体育”或“CCTV-5”
            if "#EXTINF" in lines[i]:
                # 发现关键词后，把当前行（描述行）和下一行（链接行）都加入新列表
                if i + 1 < len(lines) and lines[i+1].startswith("http"):
                    new_m3u.append(lines[i])
                    new_m3u.append(lines[i+1])
            
        with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
        print(f"成功筛选了 {len(new_m3u)//2} 个频道！")
        
    except Exception as e:
        print(f"出错啦: {e}")

if __name__ == "__main__":
    filter_sports_channels()
