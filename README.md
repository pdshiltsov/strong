# ⚡ Strongpy

A simple runtime type checker for Python functions.

It validates function arguments and return values using type annotations.

---

# 🚀 Features

- Runtime type checking for function arguments
- Return type validation
- Supports modern Python typing:
  - `list[T]`
  - `dict[K, V]`
  - `tuple`
  - `set`, `frozenset`
  - `Union` (`|`)
  - `Literal`

---

# 📦 Installation

```bash
pip install strongpy
```
or (using uv)

```bash
uv add strongpy
```

---

# 🧪 Usage

```python
from strongpy import strong

@strong
def add(x: int, y: int) -> int:
    return x + y

print(add(1, 2))   # OK
print(add("1", 2)) # TypeError
```

---

# 💥 Example error

```text
add argument 'x' expected int, got str
```

---

# 🧠 Supported types

- `int`, `str`, `float`, `bool`
- `list[T]`
- `dict[K, V]`
- `tuple[T, ...]`
- `set[T]`
- `frozenset[T]`
- `Union` (`int | str`)
- `Literal`

---

# ⚙️ Philosophy

Strong is designed to be:

- simple
- explicit
- predictable

No magic, no runtime inference — only annotations.

---

# 🐍 Requirements

Python 3.13+

---

# 📌 License

MIT
