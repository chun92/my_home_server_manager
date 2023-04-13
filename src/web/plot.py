import os
import datetime
import matplotlib.pyplot as plt

LOG_DIR = '../../log'
STATIC_DIR = 'static'

def get_data(hours):
    now = datetime.datetime.now()
    data = {'time': [], 'cpu': [], 'memory': [], 'gpu_memory_used': [], 'gpu_temperature': []}

    count = 0
    while hours > 0:
        now_date = (now.date() - datetime.timedelta(days=count)).isoformat()
        log_file = os.path.join(LOG_DIR, f'{now_date}.txt')
        
        if not os.path.exists(log_file):
            break

        with open(log_file, 'r') as f:
            for line in f:
                cols = line.strip().split('\t')
                time = now_date + ' ' + cols[0]
                data_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
                if now - data_time <= datetime.timedelta(hours=hours):
                    data['time'].append(cols[0])
                    data['cpu'].append(float(cols[1]))
                    data['memory'].append(float(cols[2]))
                    data['gpu_memory_used'].append(float(cols[3].split('/')[0]))
                    data['gpu_temperature'].append(float(cols[4]))
        
        if count == 0:
            hours -= now.hour
        else:
            hours -= 24
        count += 1

    return data

def add_subplot(index, slot, time, data, name, unit):
    plt.subplot(4, 1, index)
    plt.plot(time, data, label=name)
    plt.title(name)
    plt.xlabel('min')
    plt.ylabel(unit)
    plt.xticks([])
    x_ticks = list(range(0, len(time), slot)) + [len(time) - 1]
    x_tick_labels = [label[3:].replace(' ', ':') for i, label in enumerate(time) if i in x_ticks]
    plt.xticks(x_ticks, x_tick_labels)

def plot_graph(hours=1):
    data = get_data(hours)

    x, y1, y2, y3, y4 = data['time'], data['cpu'], data['memory'], data['gpu_memory_used'], data['gpu_temperature']
    slot = hours * 5

    plt.figure(figsize=(6, 12))
    add_subplot(1, slot, x, y1, 'CPU Percentage', '%');
    add_subplot(2, slot, x, y2, 'Memory Percentage', '%');
    add_subplot(3, slot, x, y3, 'GPU Memory Usage', 'MiB');
    add_subplot(4, slot, x, y4, 'GPU Temperature', '°C');
    plt.subplots_adjust(hspace=0.5)
    plt.savefig(os.path.join(STATIC_DIR, 'plots.png'))
    plt.close()

