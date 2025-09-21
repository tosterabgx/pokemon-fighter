class Pokemon:
    def __init__(self, name: str, atk: int = 0, df: int = 0, hp: int = 100) -> None:
        self.name = name
        self.hp = hp
        self.atk, self.df = atk, df

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, value)

    @property
    def atk(self) -> int:
        return self._atk

    @atk.setter
    def atk(self, value: int) -> None:
        self._atk = max(5, value)

    @property
    def df(self) -> int:
        return self._df

    @df.setter
    def df(self, value: int) -> None:
        self._df = max(5, value)

    def get_name(self) -> str:
        return self.name

    def get_hp(self) -> int:
        return self.hp

    def get_atk(self) -> int:
        return self.atk

    def get_def(self) -> int:
        return self.df

    def attack(self, opponent: "Pokemon") -> None:
        if self.hp > 0 and opponent.hp > 0:
            opponent.hp -= max(1, self.atk - opponent.df)


class WaterPokemon(Pokemon):
    def attack(self, opponent: Pokemon) -> None:
        if self.hp > 0 and opponent.hp > 0:
            atk = self.atk

            if isinstance(opponent, FirePokemon):
                atk *= 3

            opponent.hp -= max(1, atk - opponent.df)


class FirePokemon(Pokemon): ...


class GrassPokemon(Pokemon):
    def attack(self, opponent: Pokemon) -> None:
        if self.hp > 0 and opponent.hp > 0:
            df = opponent.df

            if isinstance(opponent, FirePokemon):
                df //= 2

            opponent.hp -= max(1, self.atk - df)


class ElectricPokemon(Pokemon):
    def attack(self, opponent: Pokemon) -> None:
        if self.hp > 0 and opponent.hp > 0:
            df = opponent.df

            if isinstance(opponent, WaterPokemon):
                df = 0

            opponent.hp -= max(1, self.atk - df)


class Trainer:
    def __init__(self):
        self.wins = 0
        self.box = []

    def add(self, pokemon: Pokemon) -> None:
        self.box.append(pokemon)

    def best_team(self, n: int) -> list[Pokemon]:
        n = min(n, len(self.box))

        team, self.box = self.box[:n], self.box[n:]

        return team
