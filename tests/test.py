from functools import wraps
from itertools import combinations, permutations
from asyncio import *
from ap_int import *
from random import randrange
from operator import *
from os import system

system('.venv\\Scripts\\activate')

class test:
    n = 0
    tests = []

    def __init__(self, name, times=1, timeout=1):
        test.n += 1
        self._id, self.name, self.times, self.timeout = test.n, name, times, timeout

    def __call__(self, f):
        @wraps(f)
        async def wrapper():
            print(end=f'Test #{self._id}: {self.name}... ')
            try:
                for _ in range(self.times):
                    if self.timeout is None:
                        f()
                    else:
                        async with timeout(self.timeout):
                            await f()
                print('Passed')
                return 0
            except TimeoutError:
                print('Failed: Timed Out')
                return 1
            except Exception as e:
                print(f'Failed: {e}')
                return 1
        test.tests.append(wrapper)
        return wrapper
    
    @classmethod
    async def execute_all(cls):
        s = cls.n
        for t in cls.tests:
            s -= await t()
        print(f'Passed {s}/{cls.n}')

def randbits(bits=1024):
    return randrange(1 << bits)

def op_test(op, a, ia):
    s, n = op(*a), len(a)
    for i in range(1, 1 << n):
        assert s == op(*(a[j] if i >> j & 1 else ia[j] for j in range(n)))
    
@test('Initialization')
async def init():
    a = randbits()
    Integer()
    Integer(a)
    Integer(str(a))

@test('Arithmetics', 3)
async def arithmetics():
    a, b = (randbits() for _ in range(3)), randbits(10)
    ia, ib = tuple(map(Integer, a)), Integer(b)
    for m, im in zip(combinations(a, 2), combinations(ia, 2)):
        for op in (add, mul):
            op_test(op, m, im)
    for m, im in zip(permutations(a, 2), permutations(ia, 2)):
        for op in (sub, floordiv):
            op_test(op, m, im)
    for m, im in zip(a, ia):
        op_test(pow, (m, b), (im, ib))
        for op in (neg, pos):
            op_test(op, (m,), (im,))
    for m, im in zip(permutations(a, 3), permutations(ia, 3)):
        op_test(pow, m, im)

@test('Bitwise', 3)
async def bitwise():
    a = (randbits(), randbits())
    ia = tuple(map(Integer, a))
    for op in (or_, and_, xor):
        op_test(op, a, ia)
    for m, im in zip(a, ia):
        op_test(inv, (m,), (im,))

run(test.execute_all())

system('deactivate')