class SmartTrainer(Trainer):
    def best_team(self, n):
        sorted_box = sorted(self.box, key=lambda pokemon: pokemon.atk + pokemon.df, reverse=True)
        best_team = sorted_box[:n]
        self.box = sorted_box[n:]
        return best_team