import argparse
import dataclasses
import inspect
from typing import Any, Dict, Type


@dataclasses.dataclass
class CheckpointConfig:
    interval: int = 1
    upload: int = 2


def train(param_1: int = 1, param_2: str = "default", param_3: CheckpointConfig = CheckpointConfig()):
    print(f"Training with param_1: {param_1.__repr__()}, param_2: {param_2.__repr__()}, param_3: {param_3}")


def add_arguments_for_function(parser, func):
    sig = inspect.signature(func)
    for param_name, param in sig.parameters.items():
        param_type = param.annotation
        default = param.default if param.default is not inspect.Parameter.empty else None
        if dataclasses.is_dataclass(param_type):
            add_arguments_for_dataclass(parser, param_type, prefix=param_name)
        else:
            parser.add_argument(f"--{param_name}", type=param_type, default=default, help=f"{param_name}: {param_type}")


def add_arguments_for_dataclass(parser, cls, prefix=""):
    for field in dataclasses.fields(cls):
        full_name = f"{prefix}.{field.name}" if prefix else field.name
        field_type = field.type
        default = field.default
        if dataclasses.is_dataclass(field_type):
            add_arguments_for_dataclass(parser, field_type, prefix=full_name)
        else:
            parser.add_argument(f"--{full_name}", type=field_type, default=default, help=f"{full_name}: {field_type}")


def construct_dataclass(cls: Type, data: Dict[str, Any]):
    init_kwargs = {}
    for field in dataclasses.fields(cls):
        if isinstance(data.get(field.name), dict):
            init_kwargs[field.name] = construct_dataclass(field.type, data[field.name])
        else:
            init_kwargs[field.name] = data.get(field.name, field.default)
    return cls(**init_kwargs)


def nested_dict(input_dict):
    result = {}
    for key, value in input_dict.items():
        parts = key.split(".")
        current_level = result
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = value
    return result


def main():
    parser = argparse.ArgumentParser(description="CLI for train function")
    add_arguments_for_function(parser, train)
    args = parser.parse_args()

    # Convert argparse Namespace to dictionary
    args_dict = vars(args)
    args_dict = {k: v for k, v in args_dict.items() if v is not None}

    # Use the nested_dict function to create a nested structure
    nested_args = nested_dict(args_dict)

    # Get the signature of the train function
    sig = inspect.signature(train)
    train_args = {}

    for param_name, param in sig.parameters.items():
        param_type = param.annotation
        if dataclasses.is_dataclass(param_type):
            # Construct data class from nested_args if available
            if param_name in nested_args:
                train_args[param_name] = construct_dataclass(param_type, nested_args[param_name])
            else:
                # Use default value if not provided in nested_args
                train_args[param_name] = param.default
        else:
            # Use value directly for non-dataclass types
            train_args[param_name] = nested_args.get(param_name, param.default)

    # Call the train function with constructed arguments
    train(**train_args)


if __name__ == "__main__":
    main()
