# ap_int
![GitHub Release](https://img.shields.io/github/v/release/cyan-ice/ap-int)
![GitHub License](https://img.shields.io/github/license/cyan-ice/ap-int)

Python package for Arbitrary-Precision arithmetic.

## Install

Execute `python3 -m pip install ap_int`.

## Contributing

### Testing (Windows)

1. Clone the Github repo.
2. Make sure you're at the source directory.
3. Execute `py test.py`.

## Documentation

### Classes

Arbitrary-Precision integer class.

Usage:
```py
>>> a, b = Integer(114514), Integer('1919810')
>>> a * b
Integer(219845122340)
>>> b // a
Integer(16)
>>> a - b
Integer(-1805296)
>>> a ** b > b ** a
True
>>> a >= b
False
>>> a ^ b
Integer(1897488)
>>> pow(a, b, 10)
Integer(6)
```
