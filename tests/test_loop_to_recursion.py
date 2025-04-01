import ast

import pytest

from loop_to_recursion.loop_to_recursion import loop_to_recursion

original_code_1 = """def function(x):
    l, r, m = 0, x + 1, 0
    while r - l != 1:
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    return l
"""
original_code_2 = """def function(x):
    l, r = 0, x + 1
    while r - l != 1:
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    return l
"""
original_code_3 = """def function(x):
    l, r = 0, x + 1
    while True:
        if r - l == 1:
            break
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    return l
"""
original_code_4 = """def function(x):
    l, r = 0, x + 1
    while True:
        if r - l == 1:
            break
        m = (r + l) // 2
        if x < m * m:
            r = m
            continue
        l = m
    return l
"""
original_code_5 = """def function(x):
    l, r = 0, x + 1
    while r - l < 10:
        if r - l == 1:
            break
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    else:
        return r
    return l
"""
original_code_6 = """def function(x):
    l, r = 0, x + 1
    while r - l < 10:
        if r - l == 1:
            return l
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    else:
        return r
"""
original_code_7 = """def function(x):
    l, r, m = 0, x + 1, 0
    while True:
        if r - l > 10:
            return r
        if r - l == 1:
            return l
        m = (r + l) // 2
        if x < m * m :
            r = m
        else:
            l = m
    raise AssertionError
"""
original_code_8 = """def function(x):
    l, r, m = 0, x + 1, 0
    while True:
        if r - l > 10:
            return r
        if r - l == 1:
            break
        m = (r + l) // 2
        if x < m * m:
            r = m
        else:
            l = m
    return l
"""
original_code_9 = """
def function(n):
    s = 0
    for i in range(n):
        if i % 12 == 0:
            break
        elif i % 6 == 0:
            continue
        elif i % 4 == 0:
            return s
        else:
            s += i
    else:
        return s + 5
    return s + 8
"""
original_code_10 = """def function(x):
    return sum(i * i for i in range(x))
"""
original_code_11 = """def function(n):
    d = 2
    table = []
    while d * d <= n:
        while n % d == 0:
            n /= d
            table.append(d)
        d += 1
    if n > 1:
        table.append(n)
    return table
"""
original_code_12 = """
def function(x):
    a = 3
    i = 1
    while i < 10:
        def function2(y):
            return y * 2
        a += function2(i)
        i += 1
    return a
"""
original_code_13 = """
def function(x):
    if x % 2 == 0:
        a = 1
        b = a
    else:
        b = sum(a for a in range(5))
    return b
"""
original_code_14 = """
def function(x):
    for i in range(x):
        for j in range(i):
            if i == j + 2:
                return 3
    return 0
"""
original_code_15 = """
def function(x):
    i, j = 0, 0
    while i < x:
        while j < i:
            if i == j + 2:
                return 3
            j += 1
        i += 1
    return 0
"""
original_code_16 = """
def function(x):
    i = 0
    while i < x:
        for j in range(x):
            if i == j + 2:
                return 3
        i += 1
    return 0
"""
original_code_17 = """
def function(x):
    j = 0
    for i in range(x):
        while j < i:
            if i == j + 2:
                return 3
            j += 1
    return 0
"""
original_code_18 = """
def function(x):
    if True:
        i = 0
    else:
        j = 0
    a = 0
    for j in range(x):
        a += i
    return a
"""
original_code_19 = """
class A:
    a = 0
def function(x):
    i = 0
    for a in range(x):
        i += a
    return i
"""
original_code_20 = """
def function(x):
    try:
        i = 0
    except:
        j = 0
        raise
    a = 0
    for j in range(x):
        a += i
    return a
"""
original_code_21 = """
def function(x):
    a = 0
    def function2(*arg, k=2, **kwargs):
        if arg[0] == 2 and kwargs['a'] == 3 and k == 2:
            a = 2
        else:
            arg = None
            kwargs = None
            k = None
            a = 3
        return a
    return function2(2, a=3)
"""
original_code_22 = """
def function(x):
    a = 0
    def function2(r, k=2, /, **kwargs):
        if r == 2 and kwargs['a'] == 3 and k == 2:
            a = 2
        else:
            r = None
            k = None
            kwargs = None
            a = 3
        return a
    return function2(2, a=3)
"""
original_code_23 = """
def function(x):
    def gen(y):
        i = 0
        while i < y:
            yield i
            i += 1
    return sum(gen(x))
"""
original_code_24 = """
def function(x):
    def gen(y):
        for i in range(y):
            yield i
    return sum(gen(x))
"""
original_code_25 = """
def function(x):
    return sum([i * i for i in range(x)])
"""
original_code_26 = """
def function(x):
    return [[i * j for j in range(i)] for i in range(x)]
"""
original_code_27 = """
def function(x):
    if x in [i for i in range(x) if i % 2 == 0]:
        return x
    else:
        return 0
"""
original_code_28 = """
def function(x):
    a = 4
    i = 0
    while i in [j for j in range(x)]:
        a += i
        i += 1
    return a
"""
original_code_29 = """
def function(x):
    a = 4
    for i in [j for j in range(x)]:
        a += i
    return a
"""
original_code_30 = """
def function(x):
    return sum([x for x in range(x)])
"""
original_code_31 = """
def function(x):
    a = 4
    i = 0
    while i in [i for i in range(x)]:
        a += i
        i += 1
    return a
"""
original_code_32 = """
def function(x):
    return {i for i in range(x) if x % 2 == 0}
"""
original_code_33 = """
def function(x):
    return {i: i * i for i in range(x) if x % 2 == 0}
"""
original_code_34 = """
import asyncio
def function(x):
    async def function2():
        async def function3():
            return 5
        return await function3()
    return asyncio.run(function2())
"""
original_code_35 = """
import asyncio
def function(x):
    async def function2():
        async def function3(x):
            return x * x
        a = 0
        for i in range(5):
            a += await function3(x)
        return a
    return asyncio.run(function2())
"""
original_code_36 = """
import asyncio
def function(x):
    async def function2():
        async def function3(x):
            return x * x
        a = 0
        i = 0
        while i < 5:
            a += await function3(x)
            i += 1
        return a
    return asyncio.run(function2())
"""
original_code_37 = """
i = 5
def function(x):
    a = 0
    for i in range(5):
        a += i
    return a
"""
original_code_38 = """def function(x):
    a = 5
    def function2():
        nonlocal a
        for i in range(5):
            a += i
        return a
    return function2()
"""
original_code_39 = """
a = 5
def function(x):
    global a
    for i in range(5):
        a += i
    return a
"""
original_code_40 = """
def function(x):
    it = range(5)
    it = (i for i in it)
    a = 0
    for i in it:
        a += i
    return a
"""
original_code_41 = """
def function(x):
    s = [i for i in undefined] if False else 3
    return s
"""
original_code_42 = """
def function(x):
    def function2():
        "DOCSTRING"
        a = 1
    return function2.__doc__
"""
original_code_43 = """
def function2():
    raise ValueError
def function(x):
    try:
        for i in range(x):
            try:
                return function2()
            except ValueError:
                return 1
    except ValueError:
        return 2
"""
original_code_44 = """
"DOCSTRING"
for i in range(5):
    __doc__ += str(i)
def function(x):
    return 4
"""
original_code_45 = """
a = 5
for i in range(5):
    a += i
def function(x):
    return a
"""
original_code_46 = """
from __future__ import annotations
a = 5
for i in range(5):
    a += i
def function(x):
    return a
"""
original_code_47 = """class A():
    "DOCSTRING"
    a = 0
    for i in range(5):
        a += i
a = A()
def function(x):
    return a.a"""
original_code_48 = """
class A():
    "DOCSTRING"
    a = 0
    i = 0
    while i < 5:
        a += i
        i += 1
a = A()
def function(x):
    return a.a
"""
original_code_49 = """
def function(x):
    async def function2():
        yield 3
        return
    return 1
"""
original_code_50 = """
import asyncio
def function(x):
    async def function2(x):
        yield 1
        yield 3
        yield 5
    async def function3():
        a = 0
        async for i in function2(x):
            a += i
            if i > 3:
                break
        return a
    return asyncio.run(function3())
"""
original_code_51 = """
import asyncio
def function(x):
    async def function2(x):
        yield 1
        yield 3
    async def function3():
        a = 0
        async for i in function2(x):
            a += i
        return a
    return asyncio.run(function3())
"""
original_code_52 = """
class A():
    a, b, c = 5, 3, 4
    for i in range(a):
        for j in range(a):
            c += b
def function(x):
    return A().b
"""


@pytest.mark.parametrize(
    "original_code",
    [
        pytest.param(original_code_1, id="1"),
        pytest.param(original_code_2, id="2"),
        pytest.param(original_code_3, id="3"),
        pytest.param(original_code_4, id="4"),
        pytest.param(original_code_5, id="5"),
        pytest.param(original_code_6, id="6"),
        pytest.param(original_code_7, id="7"),
        pytest.param(original_code_8, id="8"),
        pytest.param(original_code_9, id="9"),
        pytest.param(original_code_10, id="10"),
        pytest.param(original_code_11, id="11"),
        pytest.param(original_code_12, id="12"),
        pytest.param(original_code_13, id="13"),
        pytest.param(original_code_14, id="14"),
        pytest.param(original_code_15, id="15"),
        pytest.param(original_code_16, id="16"),
        pytest.param(original_code_17, id="17"),
        pytest.param(original_code_18, id="18"),
        pytest.param(original_code_19, id="19"),
        pytest.param(original_code_20, id="20"),
        pytest.param(original_code_21, id="21"),
        pytest.param(original_code_22, id="22"),
        pytest.param(original_code_23, id="23"),
        pytest.param(original_code_24, id="24"),
        pytest.param(original_code_25, id="25"),
        pytest.param(original_code_26, id="26"),
        pytest.param(original_code_27, id="27"),
        pytest.param(original_code_28, id="28"),
        pytest.param(original_code_29, id="29"),
        pytest.param(original_code_30, id="30"),
        pytest.param(original_code_31, id="31"),
        pytest.param(original_code_32, id="32"),
        pytest.param(original_code_33, id="33"),
        pytest.param(original_code_34, id="34"),
        pytest.param(original_code_35, id="35"),
        pytest.param(original_code_36, id="36"),
        pytest.param(original_code_37, id="37"),
        pytest.param(original_code_38, id="38"),
        pytest.param(original_code_39, id="39"),
        pytest.param(original_code_40, id="40"),
        pytest.param(original_code_41, id="41"),
        pytest.param(original_code_42, id="42"),
        pytest.param(original_code_43, id="43"),
        pytest.param(original_code_44, id="44"),
        pytest.param(original_code_45, id="45"),
        pytest.param(original_code_46, id="46"),
        pytest.param(original_code_47, id="47"),
        pytest.param(original_code_48, id="48"),
        pytest.param(original_code_49, id="49"),
        pytest.param(original_code_50, id="50"),
        pytest.param(original_code_51, id="51"),
        pytest.param(original_code_52, id="52"),
    ],
)
def test_loop_to_recursion(original_code: str) -> None:
    module = ast.parse(original_code, "<unknown>")
    context_src = {}
    exec(compile(module, "<unknown>", "exec"), context_src)
    loop_to_recursion(module)
    modified_code = ast.unparse(module)
    for node in ast.walk(module):
        assert not isinstance(node, ast.While)
        assert not isinstance(node, ast.For)
        assert not isinstance(node, ast.ListComp)
        assert not isinstance(node, ast.SetComp)
        assert not isinstance(node, ast.DictComp)
        assert not isinstance(node, ast.GeneratorExp)
    context_dst = {}
    exec(compile(module, "<unknown>", "exec"), context_dst)
    for i in range(10):
        assert context_src["function"](i) == context_dst["function"](i)
    loop_to_recursion(module)
    modified_modified_code = ast.unparse(module)
    assert modified_modified_code == modified_code


original_code_asyncgen_1 = """def function(x):
    async def function2():
        async for i in async_generator:
            yield 3
    return 1
"""
original_code_asyncgen_2 = """def function(x):
    return sum([i async for i in async_generator])
"""


@pytest.mark.parametrize(
    "original_code",
    [
        pytest.param(original_code_asyncgen_1, id="1"),
        pytest.param(original_code_asyncgen_2, id="2"),
    ],
)
def test_async_generator(original_code: str) -> None:
    module = ast.parse(original_code, "<unknown>")
    with pytest.raises(NotImplementedError):
        loop_to_recursion(module)


def test_empty() -> None:
    module = ast.parse("", "<unknown>")
    loop_to_recursion(module)
    modified_code = ast.unparse(module)
    assert modified_code == ""
