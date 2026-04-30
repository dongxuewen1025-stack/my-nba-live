import requests

def get_live_sources():
    # 这是一个社区维护的比较稳的源（通常包含CCTV及各省卫视）
    source_url = "https://ghproxy.net/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u"
    
    try:
        # 发起请求获取内容
        response = requests.get(source_url, timeout=10)
        response.raise_for_status() # 如果请求失败会抛出异常
        
        # 将获取到的几千个频道直接写入你的文件
        # 这样你的 APTV 就能看到几百个频道了
        with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("抓取成功！")
        
    except Exception as e:
        print(f"抓取失败: {e}")

if __name__ == "__main__":
    get_live_sources()
