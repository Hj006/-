import re
import csv



def extraction(input_file):

    
    name = re.split(r'[.]', input_file)[0]

    # 打开输入文件并读取内容
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 定义正则表达式提取标题、音频和视频链接
    title_pattern = r'<div[^>]*?class="title-box fwb"><a[^>]*?>([^<]+)</a></div>'
    audio_pattern_mp3 = r'<(\d+)audio[^>]*?src="(https://[^"]+\.mp3\?[^"]+)"'
    audio_pattern_mp4 = r'<(\d+)audio[^>]*?src="(https://[^"]+\.mp4\?[^"]+)"'
    video_pattern = r'<(\d+)video[^>]*?src="(https://[^"]+\.mp4\?[^"]+)"'

    # 提取标题列表
    titles = re.findall(title_pattern, content)

    # 提取音频和视频链接
    audio_links_mp3 = re.findall(audio_pattern_mp3, content)
    audio_links_mp4 = re.findall(audio_pattern_mp4, content)
    video_links = re.findall(video_pattern, content)

    # 合并音频链接 (包含 mp3 和 mp4) 和视频链接
    audio_links = audio_links_mp3 + audio_links_mp4
    links = {
        "audio": audio_links,
        "video": video_links
    }


    results = []

    for media_type, media_links in links.items():
        
        for index, link in media_links:
            index = int(index)  # 转换索引为整数
            if index > len(titles):  # 确保索引不超出标题范围
                continue
            
            title = titles[index]
            title = title.replace('\n', '')
            title = title.replace(r',', '')
            title = title.replace(r'，', '')
            
            
            if media_type == "audio":
                results.append([link, title, 'mp3'])
            elif media_type == "video":
                results.append([link, title, 'mp4'])


    output_dir = name + "_out.txt"
    with open(output_dir, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
        
    print(f"匹配结果已保存到 {output_dir}")

if __name__ == "__main__":
    input_file = r"F:\codes\脚本\afdain_v2\12蓝心音频(二).txt"
    extraction(input_file)