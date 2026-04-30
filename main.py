import requests
import time

def filter_channels():
    # 稳定源地址
    source_url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
    
    # 1. 增加重试机制 (针对之前的 Connection aborted 错误)
    max_retries = 3
    r = None
    for i in range(max_retries):
        try:
            print(f"正在连接源地址 (第 {i+1} 次)...")
            r = requests.get(source_url, timeout=20)
            r.raise_for_status()
            break 
        except Exception as e:
            print(f"连接失败: {e}")
            if i < max_retries - 1: time.sleep(5)
            else: return

    lines = r.text.split('\n')
    new_m3u = ["#EXTM3U"]
    
    # 2. 扩大关键词范围：包含央视、主流卫视和体育
    # 如果你想看更多，可以在列表里继续加关键词
    keywords = ["CCTV", "卫视", "体育", "NBA", "赛事", "篮球", "足球", "五星", "广东"]
    
    count = 0
    for i in range(len(lines)):
        # 只要这一行包含上面任何一个关键词
        if any(word.upper() in lines[i].upper() for word in keywords):
            # 确保下一行是 http 开头的链接
            if i + 1 < len(lines) and lines[i+1].startswith("http"):
                new_m3u.append(lines[i])
                new_m3u.append(lines[i+1])
                # 在日志里打印出来，让你知道抓到了什么
                print(f"已找到: {lines[i].split(',')[-1]}")
                count += 1

    # 3. 写入文件
    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"\n🎉 处理完成！总共筛选出 {count} 个频道。")

if __name__ == "__main__":
    filter_channels()
