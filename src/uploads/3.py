class SmartTrainer(Trainer):
    def best_team(self, n):
        team = self.box[:n]
        self.box = self.box[n:]
        return team
