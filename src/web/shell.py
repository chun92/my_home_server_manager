import os
import signal
import subprocess
import time
import socket

CONFIG = {}

def wait_for_port(port, timeout=60):
    start_time = time.monotonic()
    while time.monotonic() < start_time + timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                print(f"Port {port} is available now.")
                return
        except ConnectionRefusedError:
            print(f"Port {port} is not available yet.")
            time.sleep(1)
    raise TimeoutError(f"Timed out waiting for port {port} to become available.")

def set_shell_config(config):
    global CONFIG
    CONFIG = config

def kill_process_on_port(port):
    try:
        pid = int(subprocess.check_output(["lsof", "-t", "-i", f":{port}"]))
        os.kill(pid, signal.SIGTERM)
        print(f"Process running on port {port} has been terminated.")
    except subprocess.CalledProcessError:
        print(f"No process running on port {port}.")

def reboot_stable_diffusion():
    global CONFIG
    try:
        kill_process_on_port(CONFIG['port'])
        wait_for_port(CONFIG['port'], timeout=60)
        os.chdir(CONFIG['home'])
        subprocess.Popen(['/bin/bash', CONFIG['run']])
        time.sleep(5)
        return True
    except TimeoutError:
        return False
