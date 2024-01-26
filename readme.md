# Usage

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

```sh
➜ python demo.py --lr 0.01 --model.num_layers 5
0.01
5
```

