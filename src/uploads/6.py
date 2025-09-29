class SmartTrainer(Trainer):
    def sort_pokemons(self) -> None:
        self.box.sort(key=lambda x: (x.atk + x.df, x.atk, x.df), reverse=True)

    def best_team(self, n: int) -> list:
        self.sort_pokemons()

        non_fire_pokemons = []
        fire_pokemons = []
        
        for p in self.box:
            if "fire" in type(p).__name__.lower():
                fire_pokemons.append(p)
            else:
                non_fire_pokemons.append(p)

        team = non_fire_pokemons[:n]

        while len(team) < n:
            team.append(fire_pokemons[0])
            del fire_pokemons[0]
        

        self.box = [pokemon for pokemon in self.box if pokemon not in team]
        return team
