import requests
import time

def filter_sports_channels():
    # 使用更直接的源地址
    source_url = "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
    
    # 增加重试逻辑，防止网络不稳定导致连接中断
    max_retries = 3
    r = None
    
    for i in range(max_retries):
        try:
            print(f"正在尝试连接 (第 {i+1} 次)...")
            r = requests.get(source_url, timeout=20)
            r.raise_for_status()
            break 
        except Exception as e:
            print(f"连接失败: {e}")
            if i < max_retries - 1:
                time.sleep(5) # 等5秒再试
            else:
                print("达到最大重试次数，任务停止。")
                return

    lines = r.text.split('\n')
    new_m3u = ["#EXTM3U"]

    # 遍历每一行，寻找关键词
    for i in range(len(lines)):
        # 只要这一行包含你想看的关键词
        if any(word in lines[i] for word in ["CCTV-5", "体育", "NBA", "赛事", "篮球", "五星"]):
            # 把当前行（描述行）和下一行（链接行）都加入新列表
            if i + 1 < len(lines) and lines[i+1].startswith("http"):
                new_m3u.append(lines[i])
                new_m3u.append(lines[i+1])

    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(new_m3u))
    
    print(f"🎉 成功筛选了 {len(new_m3u)//2} 个频道！")

if __name__ == "__main__":
    filter_sports_channels()
