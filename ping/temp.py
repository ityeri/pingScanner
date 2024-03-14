import psutil

def countProcesses(script_name):
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'py.exe' in proc.info['name'].lower():
            cmdline = proc.info['cmdline']
            if len(cmdline) > 1 and script_name in cmdline[1]:
                count += 1
    return count

script_name = "mainPing_16bit.PY"  # 실행 중인 파이썬 스크립트의 이름을 지정하세요
count = count_running_py_processes(script_name)
print(f"{script_name} 스크립트를 실행하는 py.exe 프로세스가 {count}개 실행 중입니다.")
