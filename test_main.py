import argparse
from dataclasses import dataclass

from main import (
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
