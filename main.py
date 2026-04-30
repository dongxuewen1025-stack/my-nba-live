import requests
import datetime

def generate_nba_m3u():
    # 这里先放几个相对稳一点的体育源作为测试，以后你可以根据 Python 所学去爬取
    test_streams = [
        {"title": "CCTV-5 体育 (测试)", "url": "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8"},
        {"title": "备用 NBA 测试源", "url": "https://pili-live-hdl.vcinema.cn/vcinema/nba_stream.m3u8"}
    ]
    
    m3u_content = "#EXTM3U\n"
    for stream in test_streams:
        m3u_content += f'#EXTINF:-1 group-title="NBA", {stream["title"]}\n'
        m3u_content += f'{stream["url"]}\n'
    
    with open("my_nba_list.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("M3U文件已生成")

if __name__ == "__main__":
    generate_nba_m3u()
