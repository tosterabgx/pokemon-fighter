import random

from lib.base import (
    ElectricPokemon,
    FirePokemon,
    GrassPokemon,
    Pokemon,
    Trainer,
    WaterPokemon,
)

POKEMON_TYPES = [ElectricPokemon, FirePokemon, GrassPokemon, WaterPokemon]


class Competition:
    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2

    def _random_pokemon(
        self, idx: int, atk_max: int, df_max: int, hp_max: int, hp_min: int
    ) -> Pokemon:
        pokemon_type = random.choice(POKEMON_TYPES)

        hp = random.randint(hp_min, hp_max)
        atk = random.randint(1, atk_max)
        df = random.randint(1, df_max)

        return pokemon_type(name=f"Pokemon {idx}", atk=atk, df=df, hp=hp)

    def _duel(self, pokemon1: Pokemon, pokemon2: Pokemon) -> int:
        turn = 0 if random.random() < 0.5 else 1

        while pokemon1.hp > 0 and pokemon2.hp > 0:
            if turn == 0:
                pokemon1.attack(pokemon2)
                turn = 1
            else:
                pokemon2.attack(pokemon1)
                turn = 0

        if pokemon1.hp > 0:
            return 0
        else:
            return 1

    def fill_boxes(
        self,
        count: int = 50,
        atk_max: int = 20,
        df_max: int = 20,
        hp_max: int = 100,
        hp_min: int = 90,
    ) -> None:
        for i in range(count):
            pokemon = self._random_pokemon(i, atk_max, df_max, hp_max, hp_min)
            self.trainer1.add(pokemon)
            self.trainer2.add(pokemon)

    def compete(self, pokemon_per_team: int = 5) -> int:
        if (
            len(self.trainer1.box) < pokemon_per_team
            or len(self.trainer2.box) < pokemon_per_team
        ):
            raise IndexError("Boxes are not filled enough. Have you used fill_boxes?")

        team1 = self.trainer1.best_team(pokemon_per_team)
        team2 = self.trainer2.best_team(pokemon_per_team)

        i, j = 0, 0

        pokemon1 = team1[i]
        pokemon2 = team2[j]

        while i < len(team1) and j < len(team2):
            result = self._duel(pokemon1, pokemon2)

            if result == 0:
                j += 1
                if j >= len(team2):
                    break
                pokemon2 = team2[j]
            else:
                i += 1
                if i >= len(team1):
                    break
                pokemon1 = team1[i]

        if j >= len(team2):
            return 0
        else:
            return 1
