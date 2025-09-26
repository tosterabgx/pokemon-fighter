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


class Battle:
    @staticmethod
    def get_random_pokemon(idx: int, atk_max: int = 5, df_max: int = 5) -> Pokemon:
        pokemon_type = random.choice(POKEMON_TYPES)

        atk = random.randint(1, atk_max)
        df = random.randint(1, df_max)

        return pokemon_type(name=f"Pokemon {idx}", atk=atk, df=df)

    @staticmethod
    def duel(pokemon1: Pokemon, pokemon2: Pokemon) -> int:
        turn = 0

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

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2

    def fill_boxes(self, count: int = 50, atk_max: int = 5, df_max: int = 5) -> None:
        for i in range(count):
            pokemon = Battle.get_random_pokemon(i, atk_max=atk_max, df_max=df_max)
            self.trainer1.add(pokemon)
            self.trainer2.add(pokemon)

    def start(self, pokemon_per_team: int = 5) -> int:
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
            result = Battle.duel(pokemon1, pokemon2)

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


def do_battle_all():
    return (dict(), dict())
