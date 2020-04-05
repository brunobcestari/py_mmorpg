import pygame
from client.res.network import Network
import os

dy = 40
dx = 40


class Player:
    def __init__(self, state):
        self.connection = Network()
        self.state = state
        self.id = state["ID"]
        self.name = state["name"]
        self.pos_x = state["position"][0]
        self.pos_y = state["position"][1]
        self.pos_z = state["position"][2]
        self.health = state["health"]
        self.mana = state["mana"]
        self.stamina = state["stamina"]

    def update_position(self, new_position):
        pos = eval(self.send_pos(new_position))
        self.pos_x = pos["position"][0]
        self.pos_y = pos["position"][1]
        self.pos_z = pos["position"][2]

    def send_pos(self, pos):
        position = {"position": [pos[0], pos[1], pos[2]]}
        position = str(position)
        return self.connection.send(position)

