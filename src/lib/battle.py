import random
from json import dump

from lib.base import (
    ElectricPokemon,
    FirePokemon,
    GrassPokemon,
    Pokemon,
    Trainer,
    WaterPokemon,
)
from lib.utils import get_trainer

POKEMON_TYPES = [ElectricPokemon, FirePokemon, GrassPokemon, WaterPokemon]
WIN_FIRST = -1
WIN_SECOND = 1


class Battle:
    @staticmethod
    def get_random_pokemon(idx: int, atk_max: int = 5, df_max: int = 5) -> Pokemon:
        pokemon_type = random.choice(POKEMON_TYPES)

        atk = random.randint(1, atk_max)
        df = random.randint(1, df_max)

        return pokemon_type(name=f"Pokemon {idx}", atk=atk, df=df)

    @staticmethod
    def duel(pokemon1: Pokemon, pokemon2: Pokemon, turn: int):
        turn = 0

        while pokemon1.hp > 0 and pokemon2.hp > 0:
            if turn == 0:
                pokemon1.attack(pokemon2)
                turn = 1
            else:
                pokemon2.attack(pokemon1)
                turn = 0

        if pokemon1.hp > 0:
            return WIN_FIRST, turn
        else:
            return WIN_SECOND, turn

    def __init__(self):
        self.box = list()

    def fill_box(self, count: int = 50, atk_max: int = 5, df_max: int = 5) -> None:
        for i in range(count):
            pokemon = Battle.get_random_pokemon(i, atk_max=atk_max, df_max=df_max)
            self.box.append(pokemon)

    def start(self, trainer1, trainer2, pokemon_per_team: int = 5) -> int:
        if len(self.box) < pokemon_per_team:
            raise IndexError("Boxes are not filled enough. Have you used fill_box?")

        trainer1.box = self.box
        trainer2.box = self.box

        team1 = trainer1.best_team(pokemon_per_team)
        team2 = trainer2.best_team(pokemon_per_team)

        i, j = 0, 0

        turn = 0

        pokemon1 = team1[i]
        pokemon2 = team2[j]

        while i < len(team1) and j < len(team2):
            result, turn = Battle.duel(pokemon1, pokemon2, turn)

            if result == WIN_FIRST:
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
            return -1
        else:
            return 1


def do_battle_all(users):
    n = len(users)
    usernames = [u for _, u in users]

    trainers = [get_trainer(id) for id, _ in users]

    results = {u: {"won": [], "lost": []} for u in usernames}
    for i in range(n):
        ui, ti = usernames[i], trainers[i]
        for j in range(i + 1, n):
            uj, tj = usernames[j], trainers[j]

            r = 0

            for _ in range(100):
                battle = Battle()
                battle.fill_box()

                r += battle.start(ti, tj) - battle.start(tj, ti)

            if r < 0:
                results[ui]["won"].append(j)
                results[uj]["lost"].append(i)
            elif r > 0:
                results[uj]["won"].append(i)
                results[ui]["lost"].append(j)

    with open("results.json", mode="w") as f:
        dump(results, fp=f, indent=2)

    return usernames, results
