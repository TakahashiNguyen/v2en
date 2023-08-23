from tensorflow_model_optimization import sparsity
from translators.server import TranslatorsServer

import yaml


class Config:
    def __init__(self, key=None, value=None) -> None:
        if key is None and value is None:
            with open("config.yml") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                Config.create_subclass(self, "", config)
        else:
            Config.create_subclass(self, key, value)

    @staticmethod
    def create_subclass(self, key: str, values: any):
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, dict):
                    Config.create_subclass(self, key, Config(key, value))
                else:
                    Config.create_subclass(self, key, value)
        else:
            setattr(self, key, values)


class ExtraConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.sound_tracks = {
            "macos_startup": [
                ["F#2", "C#3", "F#3", "C#4", "F#4", "A#4"],
                [5 / 3] * 6,
                [0] * 6,
            ],
            "windows7_shutdown": [
                ["G#4", "E4", "B4", "C5"],
                [0.25, 0.25, 0.25, 0.25],
                [0.0, 0.3, 0.6, 0.9],
            ],
        }
        self.v2en.flang = self.v2en.target[:2]
        self.v2en.slang = self.v2en.target[-2:]
        self.v2en.first_path, self.v2en.second_path = (
            f"./data/{self.v2en.flang}.txt",
            f"./data/{self.v2en.slang}.txt",
        )
        self.v2en.trans_dict = TranslatorsServer().translators_dict
        self.v2en.false_allow = self.v2en.num_sent / 2 * 3
        self.training.pruning_params = {
            "pruning_schedule": sparsity.keras.PolynomialDecay(
                initial_sparsity=self.training.initial_sparsity,
                final_sparsity=self.training.final_sparsity,
                begin_step=self.training.begin_step,
                end_step=self.training.end_step,
            ),
        }
        self.main_execute = True


config = ExtraConfig()
