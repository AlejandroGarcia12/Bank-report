import psutil

for proc in psutil.process_iter(['pid', 'name']):
    if 'python' in proc.info['name']:
        print(f"Python script is running with PID: {proc.info['pid']}")