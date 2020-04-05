import pygame
from client.res.network import Network
from client.res.player import Player
pygame.init()
running = True

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

dx = 40
dy = 40
width = 48
height = 48

initial_state = {
        "ID": "id_player01",
        "name": "char1",
        "position": [0, 0, 0],
        "health": 100,
        "mana": 100,
        "stamina": 100}
player = Player(initial_state)
x = player.pos_x
y = player.pos_y
z = player.pos_z

face_orientation = 'south'  # S, N, W, E
walk_north = player.walk_north
walk_south = player.walk_south
walk_west = player.walk_west
walk_east = player.walk_east

len_animation = len(walk_north)

keys_down = {
    pygame.K_w: False,
    pygame.K_s: False,
    pygame.K_d: False,
    pygame.K_a: False
}

i = 0
fps = 60
speed = 10

waiting_count = 0
waiting_max = 100 / speed


while running:

    clock.tick(fps)
    param_division = fps // len_animation

    info = pygame.display.Info()
    sw = info.current_w
    sh = info.current_h

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys_down[event.key] = True
        elif event.type == pygame.KEYUP:
            keys_down[event.key] = False

    if keys_down[pygame.K_w]:
        if waiting_count == 0:
            y -= dy
            waiting_count = waiting_max
        face_orientation = 'north'

    if keys_down[pygame.K_s]:
        if waiting_count == 0:
            y += dy
            waiting_count = waiting_max
        face_orientation = 'south'

    if keys_down[pygame.K_d]:
        if waiting_count == 0:
            x += dx
            waiting_count = waiting_max
        face_orientation = 'east'

    if keys_down[pygame.K_a]:
        if waiting_count == 0:
            x -= dx
            waiting_count = waiting_max
        face_orientation = 'west'

    if x < 0:
        x = 0
        waiting_count = 0
    elif x + height > sw:
        x = sw - height
        waiting_count = 0

    if y < 0:
        y = 0
        waiting_count = 0
    elif y + width > sh:
        y = sh - width
        waiting_count = 0

    screen.fill([0, 0, 0])

    if waiting_count - 1 < 0:
        waiting_count = 0
    else:
        waiting_count -= 1

    if i + 1 >= fps:
        i = 0
    else:
        i += 1

    player.update_position((x, y, z))

    screen.blit(vars()[f'walk_{face_orientation}'][i // param_division], (player.pos_x, player.pos_y))
    pygame.display.flip()

print('Bye Bye!')
