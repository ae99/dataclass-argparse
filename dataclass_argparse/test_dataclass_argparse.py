import argparse
from dataclasses import dataclass

from .dataclass_argparse import (
    FunctionArgumentParser,
    add_arguments_for_dataclass,
    add_arguments_for_function,
    construct_dataclass,
    construct_function_arguments,
    nested_dict,
)


@dataclass
class Nested:
    x: int = 1


@dataclass
class DemoClass:
    a: int
    b: Nested
    c: str = "c"


def test_add_arguments_for_dataclass():
    parser = argparse.ArgumentParser()
    add_arguments_for_dataclass(parser, DemoClass)

    # check that the parser accepts all our arguments
    parser.parse_args(
        [
            "--a",
            "1",
            "--b.x",
            "2",
            "--c",
            "3",
        ]
    )


def my_func(a: int, b: Nested, c: str = "c"):
    pass


def test_add_arguments_for_function():
    parser = argparse.ArgumentParser()
    add_arguments_for_function(parser, my_func)

    # check that the parser accepts all our arguments
    parser.parse_args(
        [
            "--a",
            "1",
            "--b.x",
            "2",
            "--c",
            "3",
        ]
    )


def test_nested_dict():
    input_dict = {"a.b.c": 1, "a.b.d": 2, "a.a": 3, "b": 4}
    output_dict = {"a": {"b": {"c": 1, "d": 2}, "a": 3}, "b": 4}
    # deep equal
    assert nested_dict(input_dict) == output_dict


def test_construct_dataclass():
    input_dict = {"a": 1, "b": {"x": 2}, "c": "3"}
    output = DemoClass(a=1, b=Nested(x=2), c="3")
    result = construct_dataclass(DemoClass, input_dict)
    assert result == output

    assert result.b.x == 2


def test_constuct_function_arguments():
    input_dict = {"a": 1, "b": {"x": 2}, "c": "3"}
    output = {"a": 1, "b": Nested(x=2), "c": "3"}
    result = construct_function_arguments(my_func, input_dict)
    assert result == output

    assert result["b"].x == 2


@dataclass
class NestedDefaults:
    inner: Nested = Nested(x=5)


def nested_default(inner: Nested = Nested(x=5)):
    pass


def test_nested_defaults():
    # There's three levels of defaults:
    # 1. The default value of the field in the dataclass definition
    # 2. The default value set in the *parent*, which is more specific so should take precedence
    # 3. The final passed in value, which is the most specific so should take precedence
    input_dict = {}
    output = NestedDefaults(inner=Nested(x=5))
    result = construct_dataclass(NestedDefaults, input_dict)
    assert result == output

    assert result.inner.x == 5

    output_func = {"inner": Nested(x=5)}
    result_func = construct_function_arguments(nested_default, input_dict)
    assert result_func == output_func


def test_nested_defaults_2():
    parser = argparse.ArgumentParser()
    add_arguments_for_function(parser, nested_default)

    parsed = parser.parse_args([])
    args_dict = {k: v for k, v in vars(parsed).items()}

    assert args_dict["inner.x"] == 5


def test_function_arg_parser():
    parser = FunctionArgumentParser(my_func)
    args = parser.parse_args(["--a", "1", "--b.x", "2", "--c", "3"])
    assert args == {"a": 1, "b": Nested(x=2), "c": "3"}
