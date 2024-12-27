import requests
import csv
import os
from config import SAVE_DIR
import os

def download_url(record, log_writer: csv.writer, save_dir: str):
    
    url = record[0]
    name = record[1]
    ftype = record[2]
    url = url.replace("amp;", '')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    output_file = os.path.join(save_dir, name + rf".{ftype}")

    
    try:
        
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status() 
            with open(output_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192*3):
                    file.write(chunk)
                    
        print(f"视频下载完成，保存为: {output_file}")
        log_writer.writerow([name, 1])
        
    except requests.exceptions.RequestException as e:
        
        log_writer.writerow([name, 0])
        print(f"下载失败: {e}", file=log_writer) 
        
def download_url_v2(record, log_writer: csv.writer, save_dir: str, record_i, record_len):
    
    url = record[0]
    name = record[1]
    ftype = record[2]
    url = url.replace("amp;", '')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    output_file = os.path.join(save_dir, name + rf".{ftype}")

    
    try:
        print(f"开始下载资源-{record_i + 1}: {record[1]}, total records: {record_len}")
        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status() 
            with open(output_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192*3):
                    file.write(chunk)
                    
        print(f"视频下载完成，保存为: {output_file}")
        log_writer.writerow([name, 1])
        
    except requests.exceptions.RequestException as e:
        
        log_writer.writerow([name, 0])
        print(f"下载失败: {e}", file=log_writer) 
        
        

if __name__ == "__main__":
    download_config = r"F:\codes\脚本\aifadian\output.txt"
    f = open(download_config, 'r', encoding='utf-8')
    reader = csv.reader(f)

    for li, line in enumerate(reader):
        if li < 5:
            download_url(line)


