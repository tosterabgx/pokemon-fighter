"""Basic classes for Pokemons and the Trainer with simple team picking."""


class Pokemon:
    """Basic class for all Pokemons."""

    def __init__(
        self,
        name: str,
        atk: int = 0,
        df: int = 0,
        hp: int = 100,
    ) -> None:
        """Initialize a basic Pokemon.

        Args:
            name (str): Display name of the Pokemon
            atk (int, optional): Attack power. Defaults to 0.
            df (int, optional): Defense power. Defaults to 0.
            hp (int, optional): Hit points. Defaults to 100.
        """
        self.name = name
        self.hp = hp
        self.atk, self.df = atk, df

    @property
    def name(self) -> str:
        """Get or set Pokemon's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def hp(self) -> int:
        """Get or set Pokemon's hit points.

        If less than 0, will be set to 0
        """
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, value)

    @property
    def atk(self) -> int:
        """Get or set Pokemon's attack power.

        If less than 0, will be set to 0
        """
        return self._atk

    @atk.setter
    def atk(self, value: int) -> None:
        self._atk = max(0, value)

    @property
    def df(self) -> int:
        """Get or set Pokemon's defense power.

        If less than 0, will be set to 0
        """
        return self._df

    @df.setter
    def df(self, value: int) -> None:
        self._df = max(0, value)

    def get_name(self) -> str:
        """Get the Pokemon's name."""
        return self.name

    def attack(self, opponent: "Pokemon") -> None:
        """Attack the other pokemon, reducing their HP.

        Damage is computed as max(1, self.atk - opponent.df) if both
        Pokemons have HP > 0.

        Args:
            opponent (Pokemon): The Pokemon being attacked
        """
        if self.hp > 0 and opponent.hp > 0:
            opponent.hp -= max(1, self.atk - opponent.df)


class WaterPokemon(Pokemon):
    """Water-type Pokemon.

    Has 3x attack power against Fire-type Pokemon during an attack.
    """

    def attack(self, opponent: Pokemon) -> None:
        """Attack the other pokemon, reducing their HP.

        3x attack power against Fire-type Pokemon.

        Args:
            opponent (Pokemon): The Pokemon being attacked.
        """
        old_atk = self.atk
        if isinstance(opponent, FirePokemon):
            self.atk *= 3

        super().attack(opponent)

        self.atk = old_atk


class FirePokemon(Pokemon):
    """Fire-type Pokemon."""

    pass


class GrassPokemon(Pokemon):
    """Grass-type Pokemon.

    Halves the opponent's defense when attacking Fire-type Pokemons.
    """

    def attack(self, opponent: Pokemon) -> None:
        """Attack the other pokemon, reducing their HP.

        Halves the opponent's defense against Fire-type Pokemon.

        Args:
            opponent (Pokemon): The Pokemon being attacked.
        """
        old_df = opponent.df
        if isinstance(opponent, FirePokemon):
            opponent.df //= 2

        super().attack(opponent)

        opponent.df = old_df


class ElectricPokemon(Pokemon):
    """Electric-type Pokemon.

    Sets a Water-type opponent's defense to 0 during attack.
    """

    def attack(self, opponent: Pokemon) -> None:
        """Attack the other pokemon, reducing their HP.

        Sets the defense of Water-type Pokemons to 0 during fight

        Args:
            opponent (Pokemon): The Pokemon being attacked.
        """
        old_df = opponent.df
        if isinstance(opponent, WaterPokemon):
            opponent.df = 0

        super().attack(opponent)

        opponent.df = old_df


class Trainer:
    """Basic class for all Trainers.

    Keeps a box of Pokemons and can form a team by taking the first N.
    """

    def __init__(self) -> None:
        """Initialize a Trainer with an empty box and zero wins."""
        self.wins = 0
        self.box: list[Pokemon] = []

    def add(self, pokemon: Pokemon) -> None:
        """Add a Pokemon to the Trainer's box.

        Args:
            pokemon (Pokemon): The Pokemon to add.
        """
        self.box.append(pokemon)

    def best_team(self, n: int) -> list[Pokemon]:
        """Select the first N Pokemons from the box as the team.

        This operation removes the returned Pokemons from the box.

        Args:
            n (int): Desired team size.

        Returns:
            A list with up to N Pokemons, depending on box size.
        """
        n = min(n, len(self.box))
        team, self.box = self.box[:n], self.box[n:]
        return team
