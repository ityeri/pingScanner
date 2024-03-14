import concurrent.futures
import os
import json
from ipp import *
import time
from tqdm import tqdm
import subprocess
import sys

'''
출력 파일인 a.b.0.0-16.json 은 한 파일당 65,536 개의 IP 요청 결과를 저장한다.
요청결과가 0 일때만 성공이고 나머지는 실패.

processData 에서 1은 아무일 없음 음수이거나 0이면 핑 전송 진행중 2는 완료을 의미함
'''

os.chdir("der")

with open('processData.json', 'r') as f:
    processData = json.load(f)

processData["programCount"] += 1

with open('processData.json', 'w') as f:
    json.dump(processData, f, indent=4)

def partPing(ip: str):
    global timer
    global progressUpdateInterval

    if timer <= time.time():

        timer = time.time() + progressUpdateInterval

        parts = ip.split(".")
        # 각 부분을 정수로 변환하여 리스트에 저장
        listTypeIp = [int(part) for part in parts] #입력받은 IP 의 리스트 형태

        try:
            with open('processData.json', 'r') as f:
                processData = json.load(f)

            if processData['ipAddress'][f"{listTypeIp[0]}.{listTypeIp[1]}"] > -(listTypeIp[2] * listTypeIp[3]):
                processData['ipAddress'][f"{listTypeIp[0]}.{listTypeIp[1]}"] = -(listTypeIp[2] * listTypeIp[3])

            with open('processData.json', 'w') as f:
                json.dump(processData, f, indent=4)
        except: pass

    try:
        result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
        response = result.returncode  # 0이면 성공, 그 외에는 실패
    except subprocess.TimeoutExpired:
        response = None  # 타임아웃 발생
    return ip, response

def main(scope1, scope2):
    # 대량의 IP 주소 리스트
    ip_list = []  # 실제 IP 주소로 교체

    startTime = time.time()

    print(f'{scope1}.{scope2}.0.0-16 주소에 대한 IP 주소 생성... \n')

    ip_list = list()

    for c in range(256):
        for d in range(256):
            ip_list.append(f"{scope1}.{scope2}.{c}.{d}")

    endTime = time.time()

    print('\nIP 주소 생성완료')
    print(f"IP 생성 총 소요시간, 현재 총 소요시간: {int(endTime - startTime)}\n")
    
    midleTime = time.time()
    print(f'{scope1}.{scope2}.0.0-16 에 대한 핑 전송 시작\n')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 각 IP에 대해 ping 함수를 병렬로 실행
        IPresults = list(   tqdm(executor.map(partPing, ip_list), total=len(ip_list))   )

    endTime = time.time()
    print('\n핑 전송 완료')
    print(f"핑 전송 소요시간: {int(endTime - midleTime)} | 총 소요시간: {int(endTime - startTime)}\n")

    midleTime = time.time()
    print(f'{scope1}.{scope2}.0.0-16 에 대한 결과 집계 및 파일 저장 시작\n')

    ip_list = 0

    # 결과 집계
    backPing = {}
    for i in range(65536):
        # scope = scope1*256*256*256 + scope2*256*256
        backPing[IPresults[i][0]] = IPresults[i][1]
        
        if i%100 == 0:
            print(f"결과 집계 진행도: 65536/{i}")
    
    with open(f"{scope1},{scope2},0,0-16.json", "w") as json_file:
        json.dump(backPing, json_file, indent=4)

    endTime = time.time()
    print('\n전체 단계 완료!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(f"{scope1}.{scope2}.0.0-16 에 대한 결과 집계 및 파일 저장 소요시간: {int(endTime - midleTime)} | 총 소요시간: {int(endTime - startTime)}\n")

    return backPing



#먼저 작업할 ip 를 탐색함
with open('processData.json', 'r') as f:
    processData = json.load(f)

ipAddress = [0, 0, 0, 0]

print('작업할 IP 를 찾습니다..')

for i in range(256** 2):
    ipState = processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"]
    if ipState == 1: #ip state 가 1일땐 작업을 해야 한단 소리
        #루프를 정지하고 선택한 ip 를 작업중 상태로 등록
        processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"] = 0

        with open('processData.json', 'w') as f:
            json.dump(processData, f, indent=4)

        break
    else:
        nextIp(ipAddress)

#작업할 ip 가 없을경우 프로그램 종료
if i >= 256** 2 - 1:
    print('''이미 모든 IP 가 작업 완료되어 있습니다
프로그램을 종료 합니다.''')
    sys.exit(0)

scope1, scope2 = ipAddress[2], ipAddress[3]

print(f'''작업할 IP 를 찾았습니다!:

=====================================
|   {scope1}.{scope2}.0.0-16 범위
=====================================
''')

progressUpdateInterval = 10
timer = time.time() + progressUpdateInterval

if __name__ == "__main__":
    main(scope1, scope2)

    print(f'''

=====================================
|   {scope1}.{scope2}.0.0-16 범위 완료
=====================================

''')
    on = True
    while on:
        try:
            with open('processData.json', 'r') as f:
                processData = json.load(f)

            processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"] = 2
            processData["programCount"] -= 1

            with open('processData.json', 'w') as f:
                json.dump(processData, f, indent=4)

            on = False
        except: time.sleep(5)