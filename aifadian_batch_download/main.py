import shutil
import os
import csv
import re
from config import *
from extraction import extraction
import time
from batch_download import download_url
import sys
import argparse
from add_input import add_input



parser = argparse.ArgumentParser(description='处理带有名称的命令行参数')
parser.add_argument('-u', type=str, help='wether use log (1 or 0)', default= 1)
parser.add_argument('-ru', type=str, help='wether reset log (1 or 0)', default=0)
 
# 解析参数
args = parser.parse_args()
USE_LOG = args.u
RESTE_LOG = args.ru

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
current_date = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) 
# log_file = LOG_DIR + str(current_date) + f".csv"
log_file = os.path.join(LOG_DIR, f"log.csv")

if RESTE_LOG:
    log_f = open(log_file, 'w', newline='', encoding='utf-8')
else:
    log_f = open(log_file, 'a', newline='', encoding='utf-8')
log_writer = csv.writer(log_f)


for iput in os.listdir(INPUT_DIR):
    print(iput)
    if r"_out" in iput:
        continue
    add_input(os.path.join(INPUT_DIR, iput))
    extraction(os.path.join(INPUT_DIR, iput))

if USE_LOG:
    with open(log_file, 'r', encoding='utf-8') as logs_f:
        log_reader = csv.reader(logs_f)
        logs = list(log_reader)
        names = [l[0] for l in logs]
        res = [int(l[1]) for l in logs]
        logs = dict()
        for n, r in zip(names, res):
            logs[n] = r

for iput in os.listdir(INPUT_DIR):
    if r"_out" not in iput:
        continue
    
    f = open(os.path.join(INPUT_DIR, iput), 'r', encoding='utf-8')
    reader = csv.reader(f)
    
    ipt_name = re.split(r"[.]", iput)[0]
    save_dir = os.path.join(SAVE_DIR, ipt_name)
    save_dir = save_dir.replace("_out",'')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    records = list(reader)
    for record_i, record in enumerate(records):
        if USE_LOG and logs.get(record[1], 0) == 1:
                print(f"File ${record[1]}$ exit, skip")
                continue
        print(f"开始下载资源-{record_i + 1}: {record[1]}, total records: {len(records)}")
        download_url(record, log_writer, save_dir)

        
    # for li, line in enumerate(reader):
    #     if li < 2:
    #         if USE_LOG and logs.get(line[1], 0) == 1:
    #             print(f"File ${line[1]}$ exit, skip")
    #             continue
            
    #         down_load_url(line, log_writer, save_dir)

f.close()
log_f.close()
