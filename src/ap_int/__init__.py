'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''

from decimal import Decimal, localcontext, MAX_PREC, MAX_EMAX, MIN_EMIN, Context
from dataclasses import dataclass
from math import floor, log2
from functools import partial, total_ordering

__version__ = '0.0.1'

class Integer: ...

is_integer = lambda obj: isinstance(obj, Integer)
integer_ctx = Context(MAX_PREC, None, MIN_EMIN, MAX_EMAX)
log2_10 = log2(10)

@dataclass(frozen=True)
@total_ordering
class Integer:
    '''Arbitrary-Precision integer class.

Usage:
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
Integer(6)'''

    content: Decimal

    def __init__(self, content=0):
        with localcontext(integer_ctx):
            object.__setattr__(self, 'content', content.content if is_integer(content) else Decimal(content))
    
    def __int__(self):
        with localcontext(integer_ctx):
            return floor(self.content)
    
    def __index__(self):
        return int(self)
    
    def __str__(self):
        with localcontext(integer_ctx):
            return str(self.content)
    
    def __repr__(self):
        return f'Integer({str(self)})'
    
    def __eq__(self, value):
        with localcontext(integer_ctx):
            return self.content == (value.content if is_integer(value) else value)
    
    def __lt__(self, other):
        with localcontext(integer_ctx):
            return self.content < (other.content if is_integer(other) else other)
    
    def __pow__(self, exponent, modulus=None):
        with localcontext(integer_ctx):
            return Integer(pow(self.content, exponent.content if is_integer(exponent) else exponent, modulus.content if is_integer(modulus) else modulus))
    
    def __rpow__(self, base, modulus=None):
        return pow(base, self, modulus) if is_integer(base) else Integer(pow(base, int(self)) if modulus is None else pow(base, int(self), modulus))

    def __mul__(self, other):
        with localcontext(integer_ctx):
            return Integer(self.content * (other.content if is_integer(other) else other))
    
    def __rmul__(self, other):
        return self * other
        
    def __floordiv__(self, other):
        with localcontext(integer_ctx):
            return Integer(self.content // (other.content if is_integer(other) else other))
    
    def __rfloordiv__(self, other):
        return other // self if is_integer(other) else Integer(other // int(self))
    
    def __lshift__(self, other):
        if other < 0:
            return self >> -other
        return self * pow(Integer(2), other)
    
    def __rlshift__(self, other):
        return other << self if is_integer(other) else Integer(other << int(self))
    
    def __rshift__(self, other):
        if other < 0:
            return self << -other
        with localcontext(integer_ctx):
            if (floor(self.content.logb()) + 1) * log2_10 < other:
                return Integer(0)
        return self // pow(Integer(2), other)
    
    def __rrshift__(self, other):
        return other >> self if is_integer(other) else Integer(other >> int(self))
    
    def __neg__(self):
        with localcontext(integer_ctx):
            return Integer(-self.content)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        with localcontext(integer_ctx):
            return Integer(abs(self.content))
    
    def __add__(self, other):
        with localcontext(integer_ctx):
            return Integer(self.content + (other.content if is_integer(other) else other))
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        with localcontext(integer_ctx):
            return Integer(self.content - (other.content if is_integer(other) else other))
    
    def __rsub__(self, other):
        return -(self - other)
    
    def __or__(self, other):
        return Integer(int(self) | int(other))
    
    def __ror__(self, other):
        return self | other

    def __xor__(self, other):
        return Integer(int(self) ^ int(other))
    
    def __rxor__(self, other):
        return self ^ other
    
    def __and__(self, other):
        return Integer(int(self) & int(other))
    
    def __rand__(self, other):
        return self & other
    
    def __invert__(self):
        return -self - 1
    
    def __float__(self):
        return float(int(self))

    @property
    def numerator(self):
        return +self

    @property
    def denominator(self):
        return Integer(1)
    
    @property
    def real(self):
        return +self

    @property
    def imag(self):
        return Integer()