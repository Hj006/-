# fpath = r'F:\codes\脚本\aifadian\2.txt'

def add_input(fpath: str):
    cnt = 0  # 初始化计数器
    window_size = 40  # 窗口大小
    modified_lines = []  # 用于存储修改后的内容

    # 读取文件并处理
    with open(fpath, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            modified_line = ""  # 用于拼接当前行处理后的内容
            line_length = len(line)
            
            i = 0  # 初始化指针
            while i < line_length:
                # 截取从位置 i 开始，窗口大小为 window_size 的子字符串
                chunk = line[i: i + window_size]
                
                # 如果子字符串长度不足窗口大小，直接跳出循环
                if len(chunk) < window_size:
                    modified_line += line[i:]  # 拼接剩余内容
                    break
                
                if "<audio preload" in chunk:
                    # 匹配到音频标志，添加计数器值
                    chunk = chunk.replace("<audio preload", f"<{cnt}audio preload", 1)
                    cnt += 1  # 计数器递增
                    modified_line += chunk
                    i += window_size  # 跳过当前窗口长度
                elif "<video data" in chunk:
                    # 匹配到视频标志，添加计数器值
                    chunk = chunk.replace("<video data", f"<{cnt}video data", 1)
                    cnt += 1  # 计数器递增
                    modified_line += chunk
                    i += window_size  # 跳过当前窗口长度
                else:
                    # 未匹配的内容直接拼接
                    modified_line += line[i]
                    i += 1  # 指针移动一个字符
                
            modified_lines.append(modified_line)  # 将处理后的行存入结果列表

    # 将修改后的内容写回文件
    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)

    print(f"文件 {fpath} 已成功修改")
    print(cnt)