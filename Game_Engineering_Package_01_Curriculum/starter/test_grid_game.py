import unittest
from grid_game import GameState, step, render, replay


class GridTests(unittest.TestCase):
    def test_initial_state(self):
        self.assertEqual((GameState().x, GameState().y), (0, 0))
        self.assertFalse(GameState().won)

    def test_move(self):
        self.assertEqual(step(GameState(), "D"), GameState(1, 0, 1))

    def test_boundary_costs_turn(self):
        self.assertEqual(step(GameState(), "A"), GameState(0, 0, 1))

    def test_wall_costs_turn(self):
        self.assertEqual(step(GameState(1, 0), "D"), GameState(1, 0, 1))

    def test_invalid_command(self):
        for command in ("", "DD", "Q", "x", None):
            with self.subTest(command=command):
                with self.assertRaises(ValueError):
                    step(GameState(), command)

    def test_lowercase(self):
        self.assertEqual(step(GameState(), "s"), GameState(0, 1, 1))

    def test_winning_replay(self):
        self.assertEqual(replay("SSSSDDDDDD"), GameState(6, 4, 10))
        self.assertTrue(replay("SSSSDDDDDD").won)

    def test_after_win_is_unchanged(self):
        state = replay("SSSSDDDDDD")
        self.assertEqual(step(state, "A"), state)

    def test_replay_is_repeatable(self):
        commands = "DDSASDWWDSSSSDDDDDD"
        self.assertEqual(replay(commands), replay(commands))

    def test_render_is_observational(self):
        state = GameState()
        before = state
        first = render(state)
        self.assertEqual(first, render(state))
        self.assertEqual(state, before)
        self.assertIn("Turn 0", first)

    def test_illegal_state(self):
        for args in ((-1, 0), (2, 0), (0, 5), (0, 0, -1)):
            with self.assertRaises(ValueError):
                GameState(*args)

    def test_noninteger_state(self):
        with self.assertRaises(TypeError):
            GameState(0.5, 0)


if __name__ == "__main__":
    unittest.main()
