import ipp
import time
import json

mainData = {
    "programCount": 0,
    "ipAddress": {}
}

ipData = {}
ipAddress = [0, 0, 0, 0]
timer = time.time() + 1

for i in range(65536):
    ipData[f"{ipAddress[2]}.{ipAddress[3]}"] = 1
    ipAddress = ipp.nextIp(ipAddress)

    if timer <= time.time():
        timer = time.time() + 1
        print(f'{i / 65536 * 100}%')

mainData['ipAddress'] = ipData

with open('der/processData.json', 'w') as file:
    json.dump(mainData, file, indent=4)

print('초기화 완료')