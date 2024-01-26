# dataclass_argparse

## What is it?

A tiny 'library' that lets you turn functions and dataclasses into CLIs automatically using type annotations.

## Why?

I like defining the entrypoint to most of my scripts as a function - so that I can easily programmatically call it (e.g. a parameter sweep for a train function), and so it can be tested easily.

I also like grouping config into dataclasses for readability.

And combining the two, I hate having boilerplate like `config.param` all over my code, or manually adding arguments to an argparse parser each time I decide one needs to be configurable.

## Installation

Pull this repo, and run `pip install .`

## Usage

```python
# demo.py
from dataclasses import dataclass
from dataclass_argparse import FunctionArgumentParser

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
```

Help functions work:
```sh
➜ python demo.py --help
usage: demo.py [-h] [--lr LR] [--model.num_layers MODEL.NUM_LAYERS]

CLI for train function

options:
  -h, --help            show this help message and exit
  --lr LR               lr: <class 'float'>
  --model.num_layers MODEL.NUM_LAYERS
                        model.num_layers: <class 'int'>
```

And you can define nested properties using dot notation.
```sh
➜ python demo.py --lr 0.01 --model.num_layers 5
0.01
5
```

