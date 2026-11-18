import math
import random
import pygame
import constants as c

def gameloop():

    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    clock = pygame.time.Clock()

    # 중심을 기준으로 한 꼭짓점 좌표
    local_vertices = []

    for i in range(c.VERTEX_COUNT):
        angle = i * math.tau / c.VERTEX_COUNT

        x = c.RADIUS * math.cos(angle)
        y = c.RADIUS * math.sin(angle)

        local_vertices.append((x, y))

    # 실제 꼭짓점 위치로 벽 충돌 범위를 계산
    min_x = min(x for x, y in local_vertices)
    max_x = max(x for x, y in local_vertices)
    min_y = min(y for x, y in local_vertices)
    max_y = max(y for x, y in local_vertices)

    # 재시작할 때마다 같은 시드로 초기 속도를 생성
    rng = random.Random(c.RANDOM_SEED)
    
    # 다각형별 중심 위치와 초기 속도
    polygons = []

    for row in range(c.ROWS):
        for col in range(c.COLS):
            center_x = c.START_X + col * c.SPACING_X
            center_y = c.START_Y + row * c.SPACING_Y

            # 시작 방향을 무작위로 지정
            angle = rng.randrange(c.DIRECT_COUNT) * math.tau / c.DIRECT_COUNT

            vx = c.INITIAL_SPEED * math.cos(angle)
            vy = c.INITIAL_SPEED * math.sin(angle)

            polygon = {
                "center_x": center_x,
                "center_y": center_y,
                "vx": vx,
                "vy": vy,
            }

            polygons.append(polygon)
            


    while True:
        # 이전 프레임에서 흐른 시간 (초) / 가변시간 간격으로 속도 게산
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # 종료
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True # 재시작
                elif event.key == pygame.K_ESCAPE:
                    return False # 종료


        screen.fill(c.BACKGROUND_COLOR)

        for polygon in polygons:
            # 위치 = 이전 위치 + 속도 × 시간
            polygon["center_x"] += polygon["vx"] * dt
            polygon["center_y"] += polygon["vy"] * dt

            # 왼쪽 벽
            if polygon["center_x"] + min_x < 0:
                polygon["center_x"] = -min_x
                polygon["vx"] = abs(polygon["vx"])

            # 오른쪽 벽
            elif polygon["center_x"] + max_x > c.WIDTH:
                polygon["center_x"] = c.WIDTH - max_x
                polygon["vx"] = -abs(polygon["vx"])

            # 위쪽 벽
            if polygon["center_y"] + min_y < 0:
                polygon["center_y"] = -min_y
                polygon["vy"] = abs(polygon["vy"])

            # 아래쪽 벽
            elif polygon["center_y"] + max_y > c.HEIGHT:
                polygon["center_y"] = c.HEIGHT - max_y
                polygon["vy"] = -abs(polygon["vy"])

            # 이동한 중심을 기준으로 꼭짓점 생성
            center_x = polygon["center_x"]
            center_y = polygon["center_y"]
            radius = c.RADIUS
            vertices = []

            for i in range(c.VERTEX_COUNT):
                angle = i * math.tau / c.VERTEX_COUNT

                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                vertices.append((x, y))

            pygame.draw.polygon(screen, c.POLYGON_COLOR, vertices)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    restart = True
    while restart:
        restart = gameloop()

    pygame.quit()