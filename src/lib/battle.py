import random
from copy import deepcopy

from lib.base import ElectricPokemon, FirePokemon, GrassPokemon, Pokemon, WaterPokemon
from lib.config import NUMBER_OF_ROUNDS
from lib.db import add_competition_result
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

        trainer1.box = deepcopy(self.box)
        trainer2.box = deepcopy(self.box)

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
            return WIN_FIRST
        else:
            return WIN_SECOND


def do_battle_all(users):
    print("STARTED BATTLE")
    n = len(users)

    trainers = [get_trainer(id) for id in users]

    results = {id: {"win": [], "lose": []} for id in users}
    for i in range(n):
        ii, ti = users[i], trainers[i]
        for j in range(i + 1, n):
            ij, tj = users[j], trainers[j]

            score = [0, 0]

            for _ in range(NUMBER_OF_ROUNDS // 2):
                battle = Battle()
                battle.fill_box()

                if battle.start(ti, tj) == WIN_FIRST:
                    score[0] += 1
                else:
                    score[1] += 1

                if battle.start(tj, ti) == WIN_FIRST:
                    score[1] += 1
                else:
                    score[0] += 1

            add_competition_result(ii, ij, tuple(score))
            add_competition_result(ij, ii, tuple(score[::-1]))

            if score[0] > score[1]:
                results[ii]["win"].append(ij)
                results[ij]["lose"].append(ii)
            elif score[1] > score[0]:
                results[ij]["win"].append(ii)
                results[ii]["lose"].append(ij)

    print("FINISHED BATTLE")
    return results
