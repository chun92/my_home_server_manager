import psutil
import time
import subprocess
import re

import os
import datetime

LOG_DIR = '../../log'
LOG_FILE = f'{LOG_DIR}/system_log.txt'

def ensure_log_directory():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_file():
    ensure_log_directory()
    now = datetime.datetime.now()
    return f'{LOG_DIR}/{now.date().isoformat()}.txt'

def get_data():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)

    gpu_memory_total = 0
    gpu_memory_used = 0
    gpu_temperature = 0

    try:
        # Get GPU information using nvidia-smi command
        output = subprocess.check_output(['nvidia-smi', '-q'])
        output = output.decode('utf-8')

        # Extract memory usage information
        gpu_memory_info = re.search('FB Memory Usage\s+Total\s+:\s+(\d+)\s+MiB\s+Reserved\s+:\s+(\d+)\s+MiB\s+Used\s+:\s+(\d+)\s+MiB\s+Free\s+:\s+\d+\s+MiB', output)
        gpu_memory_total = int(gpu_memory_info.group(1))
        gpu_memory_used = int(gpu_memory_info.group(3))

        # Extract temperature information
        gpu_temperature_info = re.search('GPU Current Temp\s+:\s+(\d+)\s+C', output)
        gpu_temperature = int(gpu_temperature_info.group(1))

    except Exception as e:
        print(e)
    
    
    # Save data to log file every minute
    now = datetime.datetime.now()
    log_file = get_log_file()
    with open(log_file, 'a') as f:
        f.write(f'{now.strftime("%H:%M")}\t{cpu}\t{mem.percent}\t{gpu_memory_used}/{gpu_memory_total}\t{gpu_temperature}\n')

if __name__ == '__main__':
    while True:
        get_data()
        time.sleep(60)