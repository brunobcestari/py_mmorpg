import pygame
from client.res.network import Network
import os
from bson import ObjectId

dy = 40
dx = 40


class Player:
    def __init__(self, identifier):
        self.connection = Network(identifier)
        self.state = eval(self.connection.state)
        self.id = self.state["ID"]
        self.name = self.state["name"]
        self.pos_x = self.state["position"][0]
        self.pos_y = self.state["position"][1]
        self.pos_z = self.state["position"][2]
        self.health = self.state["health"]
        self.mana = self.state["mana"]
        self.stamina = self.state["stamina"]

        # load sprites:
        local_path = os.getcwd()
        self.walk_north = [pygame.image.load(local_path + f'/sprites/{self.name}/north_{n}.png') for n in range(3)]
        self.walk_south = [pygame.image.load(local_path + f'/sprites/{self.name}/south_{n}.png') for n in range(3)]
        self.walk_west = [pygame.image.load(local_path + f'/sprites/{self.name}/west_{n}.png') for n in range(3)]
        self.walk_east = [pygame.image.load(local_path + f'/sprites/{self.name}/east_{n}.png') for n in range(3)]

    def update_position(self, new_position):
        pos = eval(self.send_pos(new_position))
        self.pos_x = pos["position"][0]
        self.pos_y = pos["position"][1]
        self.pos_z = pos["position"][2]

    def send_pos(self, pos):
        position = {"position": [pos[0], pos[1], pos[2]]}
        position = str(position)
        return self.connection.send(position)

    def move(self, direction):
        if direction == 'up':
            self.pos_y -= 1
        elif direction == 'down':
            self.pos_y += 1
        elif direction == 'right':
            self.pos_x += 1
        elif direction == 'left':
            self.pos_x -= 1

