import unittest
import Utils
import os

import WebHost
from worlds.AutoWorld import AutoWorldRegister


class TestDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tutorials_data = WebHost.create_ordered_tutorials_file()

    def test_has_tutorial(self):
        games_with_tutorial = set(entry["gameTitle"] for entry in self.tutorials_data)
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    try:
                        self.assertIn(game_name, games_with_tutorial)
                    except AssertionError:
                        # look for partial name in the tutorial name
                        for game in games_with_tutorial:
                            if game_name in game:
                                break
                        else:
                            self.fail(f"{game_name} has no setup tutorial. "
                                      f"Games with Tutorial: {games_with_tutorial}")

    def test_has_game_info(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                safe_name = Utils.get_file_safe_name(game_name)
                target_path = Utils.local_path("WebHostLib", "static", "generated", "docs", safe_name)
                for game_info_lang in world_type.web.game_info_languages:
                    with self.subTest(game_name):
                        self.assertTrue(
                            safe_name == game_name or
                            not os.path.isfile(Utils.local_path(target_path, f'{game_info_lang}_{game_name}.md')),
                            f'Info docs have be named <lang>_{safe_name}.md for {game_name}.'
                        )
                        self.assertTrue(
                            os.path.isfile(Utils.local_path(target_path, f'{game_info_lang}_{safe_name}.md')),
                            f'{game_name} missing game info file for "{game_info_lang}" language.'
                        )
