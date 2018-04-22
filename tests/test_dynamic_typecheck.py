from pytest import raises

from typeutils import dynamic_typecheck
from typing import List, Dict, Tuple, Any


class TestClassObject:
    pass


def test_dynamic_typecheck_with_simple_types():
    @dynamic_typecheck()
    def test_args_basic(i: int, s: str, o: TestClassObject) -> None:
        pass

    obj = TestClassObject()

    test_args_basic(1, "2", obj)
    test_args_basic(1, s="2", o=obj)
    test_args_basic(1, "2", o=obj)
    test_args_basic(i=1, s="2", o=obj)
    test_args_basic(s="2", o=obj, i=1)
    test_args_basic(i=1, o=obj, s="2")

    with raises(ValueError):
        test_args_basic(1, "2", "3")

    with raises(ValueError):
        test_args_basic(1, "2", "3")

    with raises(ValueError):
        test_args_basic(1, 2, obj)

    with raises(ValueError):
        test_args_basic("1", "2", obj)

    with raises(ValueError):
        test_args_basic(1, s=2, o=obj)

    with raises(ValueError):
        test_args_basic(i="1", o=obj, s="2")

    with raises(ValueError):
        test_args_basic(i=1, o=22, s="2")


def test_dynamic_typecheck_with_string_types():
    @dynamic_typecheck()
    def test_args_with_strings(i: "int", s: "str", o: "TestClassObject") -> None:
        pass

    obj = TestClassObject()

    test_args_with_strings(1, "2", obj)
    test_args_with_strings(1, s="2", o=obj)
    test_args_with_strings(1, "2", o=obj)
    test_args_with_strings(i=1, s="2", o=obj)
    test_args_with_strings(s="2", o=obj, i=1)
    test_args_with_strings(i=1, o=obj, s="2")

    with raises(ValueError):
        test_args_with_strings(1, "2", "3")

    with raises(ValueError):
        test_args_with_strings(1, "2", "3")

    with raises(ValueError):
        test_args_with_strings(1, 2, obj)

    with raises(ValueError):
        test_args_with_strings("1", "2", obj)

    with raises(ValueError):
        test_args_with_strings(1, s=2, o=obj)

    with raises(ValueError):
        test_args_with_strings(i="1", o=obj, s="2")

    with raises(ValueError):
        test_args_with_strings(i=1, o=22, s="2")


def test_dynamic_typecheck_with_composite_types():
    @dynamic_typecheck()
    def test_composite(a: List[str], b: Dict[str, str], c: Tuple[TestClassObject, int], d: List[List[int]]) -> None:
        pass

    obj = TestClassObject()

    correct_a = ["This", "is", "ok"]
    wrong_a = ["This", "is", 45]
    correct_b = {"hello": "you"}
    wrong_b = {"No": ["wrong", "type"]}
    correct_c = (obj, 23)
    wrong_c = ("Bananas", 23)
    correct_d = [[2, 3], [4, 5]]
    wrong_d = [[2, 3], [4, [5, 6]]]

    test_composite(correct_a, correct_b, correct_c, correct_d)
    test_composite(correct_a, correct_b, correct_c, d=correct_d)
    test_composite(correct_a, correct_b, c=correct_c, d=correct_d)
    test_composite(b=correct_b, c=correct_c, d=correct_d, a=correct_a)

    with raises(ValueError):
        test_composite(wrong_a, correct_b, correct_c, correct_d)
    with raises(ValueError):
        test_composite(correct_a, wrong_b, correct_c, d=correct_d)
    with raises(ValueError):
        test_composite(correct_a, correct_b, c=wrong_c, d=correct_d)
    with raises(ValueError):
        test_composite(b=correct_b, c=correct_c, d=wrong_d, a=correct_a)


def test_return_values():
    pass


def test_mixed_kwargs():
    pass


def test_benchmark():
    pass
