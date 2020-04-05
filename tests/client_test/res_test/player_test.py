import unittest
from client.res.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_state = {
             "ID": "id_player01",
             "name": "character_name",
             "position": (0, 0, 0),
             "health": 100,
             "mana": 100,
             "stamina": 100}
        self.player = Player(self.initial_state)

    def test_state(self):
        self.assertEqual(self.player.state, self.initial_state)
        self.assertEqual(self.player.pos_x, self.initial_state["position"][0])
        self.assertEqual(self.player.pos_y, self.initial_state["position"][1])
        self.assertEqual(self.player.pos_z, self.initial_state["position"][2])
        self.assertEqual(self.player.id , self.initial_state["ID"])
        self.assertEqual(self.player.name, self.initial_state["name"])
        self.assertEqual(self.player.mana, self.initial_state["mana"])
        self.assertEqual(self.player.health, self.initial_state["health"])
        self.assertEqual(self.player.stamina, self.initial_state["stamina"])

    def test_update_position(self):
        new_position = (1, 2, 3)
        self.player.update_position(new_position)
        self.player.pos_x = 1
        self.player.pos_y = 2
        self.player.pos_z = 3


if __name__ == '__main__':
    unittest.main()
