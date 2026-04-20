from typing import Literal, Any, Never, NoReturn

import pytest

from strongpy import strong

# ============================================================================
# FUNCTIONS UNDER TEST
# ============================================================================


@strong
def add(a: int, b: int) -> int:
    return a + b


@strong
def bad_return(a: int) -> str:
    return a


@strong
def sum_list(xs: list[int]) -> int:
    return sum(xs)


@strong
def total(d: dict[str, int]) -> int:
    return sum(d.values())


@strong
def mix(a: int, b: list[int], c: dict[str, int]) -> int:
    return a + sum(b) + sum(c.values())


@strong
def empty_list(xs: list[int]) -> int:
    return len(xs)


@strong
def f5(x: list[list[int]]) -> int:
    return sum(sum(row) for row in x)


@strong
def f6(d: dict[str, list[int]]) -> int:
    return sum(sum(v) for v in d.values())


@strong
def f7(x: list[int]) -> int:
    return len(x)


@strong
def f8(x: int) -> int:
    return x


@strong
def f10(a, b):
    return a + b


@strong
def u1(x: int | str) -> str:
    return str(x)


@strong
def u2(xs: list[int | str]) -> int:
    return len(xs)


@strong
def u3(d: dict[str, int | str]) -> int:
    return len(d)


@strong
def l1(mode: Literal["GET", "POST"]) -> str:
    return mode


@strong
def l2(x: Literal[1, 2, 3], y: int) -> int:
    return x + y


@strong
def t1(x: tuple[int, str, str]) -> str:
    return x[1]


@strong
def t2(x: tuple[int, ...]) -> int:
    return sum(x)


@strong
def t3(x: tuple[int, tuple[str, int]]) -> str:
    return x[1][0]


@strong
def t4(x: tuple[int | str, int]) -> int:
    return x[1]


@strong
def s1(a: list[int | str], b: dict[str, tuple[int, str]], c: tuple[int, ...]) -> int:
    return len(a) + len(b) + len(c)


# ============================================================================
# BASIC TESTS
# ============================================================================


def test_add():
    assert add(1, 2) == 3

    with pytest.raises(Exception):
        add(1, "2")


def test_bad_return():
    with pytest.raises(Exception):
        bad_return(10)


# ============================================================================
# LIST / DICT / MIX
# ============================================================================


@pytest.mark.parametrize(
    "xs, should_fail",
    [
        ([1, 2, 3], False),
        ([1, "2", 3], True),
    ],
)
def test_sum_list(xs, should_fail):
    if should_fail:
        with pytest.raises(Exception):
            sum_list(xs)
    else:
        assert sum_list(xs) == 6


def test_dict():
    assert total({"a": 1, "b": 2}) == 3

    with pytest.raises(Exception):
        total({1: 1, "b": 2})

    with pytest.raises(Exception):
        total({"a": "1"})


def test_mix():
    assert mix(1, [1, 2], {"x": 3}) == 7

    with pytest.raises(Exception):
        mix(1, [1, "2"], {"x": 3})


# ============================================================================
# EDGE CASES
# ============================================================================


def test_empty_and_misc():
    assert empty_list([]) == 0
    assert f8(True) == 1  # bool is int in Python


# ============================================================================
# NESTED STRUCTURES
# ============================================================================


def test_nested():
    assert f5([[1, 2], [3]]) == 6

    with pytest.raises(Exception):
        f5([[1, "2"], [3]])

    assert f6({"a": [1, 2], "b": [3]}) == 6

    with pytest.raises(Exception):
        f6({"a": [1, "2"]})


# ============================================================================
# INVALID INPUT TYPES
# ============================================================================


@pytest.mark.parametrize(
    "value",
    [
        None,
        "123",
        (1, 2, 3),
    ],
)
def test_invalid_list_inputs(value):
    with pytest.raises(Exception):
        f7(value)


# ============================================================================
# UNION TYPES
# ============================================================================


def test_unions():
    assert u1(10) == "10"
    assert u1("hello") == "hello"

    with pytest.raises(Exception):
        u1(1.5)

    assert u2([1, "a", 3]) == 3

    with pytest.raises(Exception):
        u2([1, 2.5])

    assert u3({"a": 1, "b": "x"}) == 2

    with pytest.raises(Exception):
        u3({"a": 1.5})


# ============================================================================
# LITERALS
# ============================================================================


def test_literals():
    assert l1("GET") == "GET"
    assert l1("POST") == "POST"

    with pytest.raises(Exception):
        l1("PUT")

    assert l2(2, 10) == 12

    with pytest.raises(Exception):
        l2(5, 10)


# ============================================================================
# TUPLES
# ============================================================================


def test_tuples():
    assert t1((1, "a", "b")) == "a"

    with pytest.raises(Exception):
        t1((1, 2, "b"))

    with pytest.raises(Exception):
        t1((1, "a"))

    assert t2((1, 2, 3)) == 6
    assert t2(()) == 0

    with pytest.raises(Exception):
        t2((1, "2"))

    assert t3((1, ("a", 2))) == "a"

    with pytest.raises(Exception):
        t3((1, ("a", "b")))

    assert t4((1, 2)) == 2
    assert t4(("a", 2)) == 2

    with pytest.raises(Exception):
        t4((1.5, 2))


# ============================================================================
# STRESS CASE
# ============================================================================


def test_stress():
    assert s1([1, "x", 3], {"a": (1, "b")}, (1, 2, 3)) == 7

    with pytest.raises(Exception):
        s1([1, 2.5], {"a": (1, "b")}, (1, 2))

    with pytest.raises(Exception):
        s1([1, "x"], {"a": (1, 2)}, (1, 2))


# ============================================================================
# SETS
# ============================================================================


@strong
def f_set_int(x: set[int]) -> int:
    return sum(x)


@strong
def f_set_str(x: set[str]) -> str:
    return ",".join(sorted(x))


@strong
def f_set_any(x: set):
    return x


@strong
def f_set_nested(x: set[tuple[int, str]]):
    return x


@strong
def f_bad_return_set() -> set[int]:
    return {"a", "b"}


def test_sets():
    assert f_set_int({1, 2, 3}) == 6
    assert f_set_int(set()) == 0

    with pytest.raises(Exception):
        f_set_int({"1", "2"})

    with pytest.raises(Exception):
        f_set_int({1, "2"})

    assert f_set_str({"a", "b"}) == "a,b"
    assert isinstance(f_set_any({1, "a"}), set)

    assert f_set_nested({(1, "a"), (2, "b")}) == {(1, "a"), (2, "b")}

    with pytest.raises(Exception):
        f_set_nested({(1, "a"), (2, 3)})

    assert f_set_int({True, False}) is not None
    assert f_set_int(set(range(1000))) is not None
    assert f_set_int({-1, -2, -3}) == -6

    with pytest.raises(Exception):
        f_bad_return_set()


# ============================================================================
# FROZENSET
# ============================================================================


@strong
def f_frozenset_int(x: frozenset[int]) -> int:
    return sum(x)


@strong
def f_frozenset_str(x: frozenset[str]) -> str:
    return ",".join(sorted(x))


@strong
def f_frozenset_any(x: frozenset):
    return x


@strong
def f_frozenset_nested(x: frozenset[tuple[int, str]]):
    return x


@strong
def f_bad_return_frozenset() -> frozenset[int]:
    return frozenset(["a", "b"])


def test_frozensets():
    assert f_frozenset_int(frozenset([1, 2, 3])) == 6
    assert f_frozenset_int(frozenset()) == 0

    with pytest.raises(Exception):
        f_frozenset_int(frozenset(["1", "2"]))

    with pytest.raises(Exception):
        f_frozenset_int(frozenset([1, "2"]))

    assert f_frozenset_str(frozenset(["a", "b"])) == "a,b"
    assert isinstance(f_frozenset_any(frozenset([1, "a"])), frozenset)

    assert f_frozenset_nested(frozenset([(1, "a"), (2, "b")])) is not None

    with pytest.raises(Exception):
        f_frozenset_nested(frozenset([(1, "a"), (2, 3)]))

    assert f_frozenset_int(frozenset([True, False])) is not None
    assert f_frozenset_int(frozenset(range(1000))) is not None
    assert f_frozenset_int(frozenset([0, 0, 0])) == 0

    with pytest.raises(Exception):
        f_bad_return_frozenset()


# ============================================================================
# TESTS FOR Any
# ============================================================================

@strong
def accept_any(x: Any) -> Any:
    return x


def test_any_with_int():
    assert accept_any(123) == 123


def test_any_with_str():
    assert accept_any("hello") == "hello"


def test_any_with_list():
    assert accept_any([1, 2, 3]) == [1, 2, 3]


def test_any_with_dict():
    assert accept_any({"a": 1}) == {"a": 1}


def test_any_with_none():
    assert accept_any(None) is None


# ============================================================================
# TESTS FOR Never (arguments)
# ============================================================================

@strong
def accept_never(x: Never):
    return x


def test_never_argument_always_fails_int():
    with pytest.raises(TypeError):
        accept_never(123)


def test_never_argument_always_fails_none():
    with pytest.raises(TypeError):
        accept_never(None)


def test_never_argument_always_fails_object():
    with pytest.raises(TypeError):
        accept_never(object())


# ============================================================================
# TESTS FOR Never (return)
# ============================================================================

@strong
def return_never() -> Never:
    return 42  # явно неверно


def test_never_return_always_fails():
    with pytest.raises(TypeError):
        return_never()


# ============================================================================
# MIXED TESTS
# ============================================================================

@strong
def any_to_int(x: Any) -> int:
    return x


def test_any_to_int_valid():
    assert any_to_int(10) == 10


def test_any_to_int_invalid():
    with pytest.raises(TypeError):
        any_to_int("not int")


@strong
def int_to_any(x: int) -> Any:
    return x


def test_int_to_any_valid():
    assert int_to_any(5) == 5


def test_int_to_any_invalid_argument():
    with pytest.raises(TypeError):
        int_to_any("oops")

# ============================================================================
# TESTS FOR NoReturn (arguments)
# ============================================================================

@strong
def accept_noreturn(x: NoReturn):
    return x


def test_noreturn_argument_always_fails_int():
    with pytest.raises(TypeError):
        accept_noreturn(123)


def test_noreturn_argument_always_fails_none():
    with pytest.raises(TypeError):
        accept_noreturn(None)


def test_noreturn_argument_always_fails_object():
    with pytest.raises(TypeError):
        accept_noreturn(object())


# ============================================================================
# TESTS FOR NoReturn (return)
# ============================================================================

@strong
def return_noreturn() -> NoReturn:
    return 42  # явно неверно


def test_noreturn_return_always_fails():
    with pytest.raises(TypeError):
        return_noreturn()


# ============================================================================
# VALID NoReturn USAGE (important edge case)
# ============================================================================

@strong
def valid_noreturn() -> NoReturn:
    raise RuntimeError("This function never returns")


def test_noreturn_valid_behavior():
    with pytest.raises(RuntimeError):
        valid_noreturn()


# ============================================================================
# MIXED TESTS (interaction with Any)
# ============================================================================

@strong
def any_to_noreturn(x: Any) -> NoReturn:
    return x  # всегда ошибка


def test_any_to_noreturn_always_fails():
    with pytest.raises(TypeError):
        any_to_noreturn(10)


@strong
def noreturn_to_any(x: NoReturn) -> Any:
    return x


def test_noreturn_to_any_always_fails():
    with pytest.raises(TypeError):
        noreturn_to_any(10)