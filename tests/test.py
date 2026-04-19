from strong import strong


def run_test(name, func, *args, should_raise=False):
    try:
        result = func(*args)
        if should_raise:
            print(f"[FAIL] {name} — expected error, got {result}")
        else:
            print(f"[OK] {name} — result: {result}")
    except Exception as e:
        if should_raise:
            print(f"[OK] {name} — raised {type(e).__name__}: {e}")
        else:
            print(f"[FAIL] {name} — unexpected error: {e}")

@strong
def add(a: int, b: int) -> int:
    return a + b


run_test("int + int", add, 1, 2)
run_test("int + str", add, 1, "2", should_raise=True)

@strong
def bad_return(a: int) -> str:
    return a  # ❌ wrong type


run_test("return type wrong", bad_return, 10, should_raise=True)

@strong
def sum_list(xs: list[int]) -> int:
    return sum(xs)


run_test("list[int] ok", sum_list, [1, 2, 3])
run_test("list[int] bad", sum_list, [1, "2", 3], should_raise=True)

@strong
def total(d: dict[str, int]) -> int:
    return sum(d.values())


run_test("dict ok", total, {"a": 1, "b": 2})
run_test("dict bad key", total, {1: 1, "b": 2}, should_raise=True)
run_test("dict bad value", total, {"a": "1"}, should_raise=True)

@strong
def mix(a: int, b: list[int], c: dict[str, int]) -> int:
    return a + sum(b) + sum(c.values())


run_test(
    "mixed ok",
    mix,
    1,
    [1, 2],
    {"x": 3}
)

@strong
def empty_list(xs: list[int]) -> int:
    return len(xs)


run_test("empty list", empty_list, [])


@strong
def f5(x: list[list[int]]) -> int:
    return sum(sum(row) for row in x)

run_test("nested ok", f5, [[1, 2], [3]])
run_test("nested fail", f5, [[1, "2"], [3]], should_raise=True)


@strong
def f6(d: dict[str, list[int]]) -> int:
    return sum(sum(v) for v in d.values())

run_test("complex ok", f6, {"a": [1, 2], "b": [3]})
run_test("complex fail", f6, {"a": [1, "2"]}, should_raise=True)


@strong
def f7(x: list[int]) -> int:
    return len(x)

run_test("None list fail", f7, None, should_raise=True)
run_test("string instead list", f7, "123", should_raise=True)
run_test("tuple instead list", f7, (1, 2, 3), should_raise=True)


@strong
def f8(x: int) -> int:
    return x

run_test("bool as int", f8, True)


@strong
def f9(a: int, b: list[int], c: dict[str, int]) -> int:
    return a + sum(b) + sum(c.values())

run_test("mixed ok", f9, 1, [1, 2], {"x": 3})
run_test("mixed fail", f9, 1, [1, "2"], {"x": 3}, should_raise=True)


@strong
def f10(a, b):
    return a + b

run_test("no annotations", f10, 1, 2)

@strong
def u1(x: int | str) -> str:
    return str(x)

run_test("union int", u1, 10)
run_test("union str", u1, "hello")
run_test("union fail", u1, 1.5, should_raise=True)

@strong
def u2(xs: list[int | str]) -> int:
    return len(xs)

run_test("list union ok", u2, [1, "a", 3])
run_test("list union fail", u2, [1, 2.5], should_raise=True)

@strong
def u3(d: dict[str, int | str]) -> int:
    return len(d)

run_test("dict union ok", u3, {"a": 1, "b": "x"})
run_test("dict union fail", u3, {"a": 1.5}, should_raise=True)

from typing import Literal

@strong
def l1(mode: Literal["GET", "POST"]) -> str:
    return mode

run_test("literal ok GET", l1, "GET")
run_test("literal ok POST", l1, "POST")
run_test("literal fail", l1, "PUT", should_raise=True)

@strong
def l2(x: Literal[1, 2, 3], y: int) -> int:
    return x + y

run_test("literal mix ok", l2, 2, 10)
run_test("literal mix fail", l2, 5, 10, should_raise=True)

@strong
def t1(x: tuple[int, str, str]) -> str:
    return x[1]

run_test("tuple fixed ok", t1, (1, "a", "b"))
run_test("tuple fixed fail type", t1, (1, 2, "b"), should_raise=True)
run_test("tuple fixed fail length", t1, (1, "a"), should_raise=True)

@strong
def t2(x: tuple[int, ...]) -> int:
    return sum(x)

run_test("tuple var ok", t2, (1, 2, 3, 4))
run_test("tuple var empty", t2, ())
run_test("tuple var fail", t2, (1, "2"), should_raise=True)

@strong
def t3(x: tuple[int, tuple[str, int]]) -> str:
    return x[1][0]

run_test("tuple nested ok", t3, (1, ("a", 2)))
run_test("tuple nested fail", t3, (1, ("a", "b")), should_raise=True)

@strong
def t4(x: tuple[int | str, int]) -> int:
    return x[1]

run_test("tuple union ok", t4, (1, 2))
run_test("tuple union ok2", t4, ("a", 2))
run_test("tuple union fail", t4, (1.5, 2), should_raise=True)

@strong
def s1(
    a: list[int | str],
    b: dict[str, tuple[int, str]],
    c: tuple[int, ...]
) -> int:
    return len(a) + len(b) + len(c)

run_test(
    "stress ok",
    s1,
    [1, "x", 3],
    {"a": (1, "b")},
    (1, 2, 3)
)

run_test(
    "stress fail list",
    s1,
    [1, 2.5],
    {"a": (1, "b")},
    (1, 2),
    should_raise=True
)

run_test(
    "stress fail dict",
    s1,
    [1, "x"],
    {"a": (1, 2)},
    (1, 2),
    should_raise=True
)

