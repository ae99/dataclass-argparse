from dataclasses import dataclass

from main import FunctionArgumentParser


@dataclass
class ModelConfig:
    num_layers: int = 3


def train(
    lr: float = 0.001,
    model: ModelConfig = ModelConfig(),
):
    print(lr)
    print(model.num_layers)


if __name__ == "__main__":
    parser = FunctionArgumentParser(train, description="CLI for train function")
    train_args = parser.parse_args()
    train(**train_args)
