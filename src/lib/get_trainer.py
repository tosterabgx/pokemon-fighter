from lib.base import Pokemon, Trainer


def get_trainer_class(code: str) -> None | Trainer:
    sandbox = {}

    try:
        exec(code, {"__builtins__": None, "abs": abs}, sandbox)
    except Exception as e:
        return None

    if "SmartTrainer" not in sandbox:
        return None

    trainer_class = sandbox["SmartTrainer"]

    try:
        trainer = trainer_class()

        trainer.add(Pokemon("test"))

        trainer.best(1)[0]
    except Exception as e:
        return None

    return trainer_class
