# import pygame

# screen = pygame.display.set_mode((600, 600))
# pygame.display.set_caption("프랙탈 맵퍼")

# SIZE = 65536

def maping(pos):
    """IP 주소를 2D 평면상에 맵핑하는 함수입니다.

IP 주소는 리스트이며 주소가 a.b.c.d 라면 입력은 [a, b, c, d] 의 형태 입니다
맵핑은 왼쪽 위부터 프랙탈 형태로 맵핑되며 
좌표는 x, y 0 ~ 65,535 의 범위를 가집니다.
"""

    dpos = [4096 * (pos[0] % 16), 4096 * pos[0] // 16]

    dpos = [dpos[0] + 256 * (pos[1] % 16), dpos[1] + 256 * pos[1] // 16]

    dpos = [dpos[0] + 16 * (pos[2] % 16), dpos[1] + 16 * pos[2] // 16]

    dpos = [dpos[0] + (pos[3] % 16), dpos[1] + pos[3] // 16]

    return dpos

def nextIp(ip):
    """입력받은 IP 주소를 한번 업카운트 하는 함수 입니다

IP 주소는 리스트이며 주소가 a.b.c.d 라면 입력은 [a, b, c, d] 의 형태 입니다
마지막 자리가 우선적으로 카운트 되며 
특정 자리가 255 를 넘을시 해당 자리는 0으로 초기화 하고 
그 이전 자리를 1만큼 올리는 방식입니다.
"""

    ip[3] += 1

    if ip[3] > 255:
        ip[3] = 0
        ip[2] += 1
    if ip[2] > 255:
        ip[2] = 0
        ip[1] += 1
    if ip[1] > 255:
        ip[1] = 0
        ip[0] += 1
    if ip[0] > 255:
        ip[0] = 0

    return ip