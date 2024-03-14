import subprocess
import time
import json
from ipp import *
import pygame
import psutil
import itWorkSpace
# import pika


'''
출력 파일인 a.b.0.0-16.json 은 한 파일당 65,536 개의 IP 요청 결과를 저장한다.
요청결과가 0 일때만 성공이고 나머지는 실패.

processData 에서 1은 아무일 없음 음수이거나 0이면 핑 전송 진행중 2는 완료을 의미함
'''

#TODO: 진행도 바 만들기 (서페이스는 있음 프로세스 하나당 바 크기는 10픽셀)

def countProcesses(script_name):
    count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'py.exe' in proc.info['name'].lower():
            cmdline = proc.info['cmdline']
            if len(cmdline) > 1 and script_name in cmdline[1]:
                count += 1
    return count

pygame.init()

screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
progressBar = pygame.Surface((256 * 10, 256 * 10))

print('작업 초기화...')

with open('der/processData.json', 'r') as f:
    processData = json.load(f)

processData['programCount'] = 0

ipAddress = [0, 0, 0, 0]

for i in range(256** 2):
    ipState = processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"]

    if ipState <= 0:
        processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"] = 1

    nextIp(ipAddress)

with open('der/processData.json', 'w') as f:
    json.dump(processData, f, indent=4)

print('작업 시작')

excuteInterval = 2
updateInterval = 5
maxPogramCount = 6

excuteTimer = time.time() + excuteInterval
updateTimer = time.time() + updateInterval
on = True

while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False

    
    if time.time() >= excuteTimer:
        excuteTimer = time.time() + excuteInterval

        programCount = countProcesses('mainPing_16bit.PY')
        
        if programCount < maxPogramCount:
            subprocess.run("start mainPing_16bit.PY", shell=True)

    if time.time() >= updateTimer:
        print('진행도 업데이트 시작')

        try:
            with open('der/processData.json', 'r') as f:
                processData = json.load(f)
        except: 
            print('├ 업데이트 실패')
            pass

        updateTimer = time.time() + updateInterval

        ipAddress = [0, 0, 0, 0]
        progressBar.fill((0, 0, 0))

        for i in range(256 ** 2):
            ipState = processData['ipAddress'][f"{ipAddress[2]}.{ipAddress[3]}"]

            x = ipAddress[3] % 256 * 10
            y = ipAddress[2] % 256 * 10

            # print(x, y)

            if ipState == 1: #아무일 없으면 검정으로 채움
                pygame.draw.rect(progressBar, (100, 0, 0), (x, y, 10, 10))
            elif ipState == 2: #완료되면 연두색
                pygame.draw.rect(progressBar, (20, 255, 20), (x, y, 10, 10))
            elif ipState <= 0: #진행중이면 파란색 크기로 진행도 표시
                progress = -ipState / (256**2) * 255
                pygame.draw.rect(progressBar, (0, 0, itWorkSpace.clamp(int(progress), 0, 255)), (x, y, 10, 10))

            pass

            nextIp(ipAddress)

        print('└ 진행도 업데이트 끝\n')

    screen.fill((0, 0, 0))

    screen.blit(
        pygame.transform.scale(progressBar, screen.get_size()), (0, 0)
    )

    pygame.display.update()