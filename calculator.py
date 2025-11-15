import math
import cmath
import sys
from fractions import Fraction
from collections import deque

try:
    import numpy as np
    HAS_NUMPY = True
except Exception:
    HAS_NUMPY = False

try:
    import sympy as sp
    HAS_SYMPY = True
except Exception:
    HAS_SYMPY = False

SAFE_NAMES = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
SAFE_NAMES.update({
    'complex': complex,
    'Fraction': Fraction,
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'pow': pow,
    'sqrt': math.sqrt,
    'pi': math.pi,
    'e': math.e,
    'i': 1j,
})

HISTORY = deque(maxlen=200)

def safe_eval(expr):
    try:
        result = eval(expr, {'__builtins__': {}}, SAFE_NAMES)
        return result
    except Exception as e:
        return f"Error: {e}"

def solve_quadratic(a, b, c):
    a, b, c = float(a), float(b), float(c)
    disc = b*b - 4*a*c
    if disc >= 0:
        r1 = (-b + math.sqrt(disc)) / (2*a)
        r2 = (-b - math.sqrt(disc)) / (2*a)
    else:
        r1 = (-b + cmath.sqrt(disc)) / (2*a)
        r2 = (-b - cmath.sqrt(disc)) / (2*a)
    return (r1, r2)

def factorial(n):
    n = int(n)
    if n < 0:
        return "Error: factorial of negative"
    return math.factorial(n)

def nPr(n, r):
    n, r = int(n), int(r)
    if r > n or n < 0:
        return "Error: invalid n/r"
    return math.perm(n, r) if hasattr(math, 'perm') else math.factorial(n)//math.factorial(n-r)

def nCr(n, r):
    n, r = int(n), int(r)
    if r > n or n < 0:
        return "Error: invalid n/r"
    return math.comb(n, r) if hasattr(math, 'comb') else math.factorial(n)//(math.factorial(r)*math.factorial(n-r))

def base_convert(num_str, b_from, b_to):
    b_from = int(b_from); b_to = int(b_to)
    try:
        val = int(str(num_str), b_from)
    except Exception as e:
        return f"Error parsing number: {e}"
    if b_to == 10:
        return str(val)
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if val == 0:
        return '0'
    sign = ''
    if val < 0:
        sign = '-'
        val = -val
    res = ''
    while val:
        res = digits[val % b_to] + res
        val //= b_to
    return sign + res

def bit_operation(op, a, b):
    a = int(a); b = int(b)
    if op == 'and':
        return a & b
    if op == 'or':
        return a | b
    if op == 'xor':
        return a ^ b
    if op == 'lshift':
        return a << b
    if op == 'rshift':
        return a >> b
    return 'Unknown bit op'

def matrix_mode():
    if not HAS_NUMPY:
        print('NumPy not available.')
        return
    print('Entering matrix mode.')
    mats = {}
    while True:
        try:
            line = input('matrix> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting matrix mode')
            return
        if not line:
            continue
        if line in ('back', 'exit'):
            print('Leaving matrix mode')
            return
        parts = line.split()
        cmd = parts[0]
        try:
            if cmd == 'new':
                name = parts[1]
                rows = int(parts[2]); cols = int(parts[3])
                vals = [float(x) for x in ' '.join(parts[4:]).replace(',', ' ').split()]
                if len(vals) != rows*cols:
                    print('Value count mismatch')
                    continue
                mats[name] = np.array(vals).reshape((rows, cols))
                print(f'Matrix {name} stored')
            elif cmd == 'show':
                name = parts[1]
                print(mats[name])
            elif cmd == 'add':
                a, b, out = parts[1], parts[2], parts[3]
                mats[out] = mats[a] + mats[b]
                print('Stored as', out)
            elif cmd == 'mul':
                a, b, out = parts[1], parts[2], parts[3]
                mats[out] = mats[a].dot(mats[b])
                print('Stored as', out)
            elif cmd == 'inv':
                name = parts[1]; out = parts[2]
                mats[out] = np.linalg.inv(mats[name])
                print('Stored as', out)
            elif cmd == 'det':
                name = parts[1]
                print(np.linalg.det(mats[name]))
            elif cmd == 'list':
                for k in mats:
                    print(k, mats[k].shape)
            else:
                print('Unknown matrix cmd')
        except Exception as e:
            print('Error:', e)

def sym_mode(expr, var='x'):
    if not HAS_SYMPY:
        return 'Sympy not available.'
    try:
        x = sp.symbols(var)
        f = sp.sympify(expr)
        simp = sp.simplify(f)
        deriv = sp.diff(f, x)
        integ = sp.integrate(f, x)
        return {'simplified': str(simp), 'derivative': str(deriv), 'integral': str(integ)}
    except Exception as e:
        return f'Error in sympy: {e}'

def repl():
    print('Complex Calculator REPL — type help for commands')
    while True:
        try:
            line = input('>>> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye')
            return
        if not line:
            continue
        HISTORY.append(line)
        if line.lower() in ('exit', 'quit'):
            print('Bye')
            return
        if line.lower() == 'help':
            print('help, eval, quad, fact, perm, comb, baseconv, bit, matrix, sym, history')
            continue
        if line.lower() == 'history':
            for i, h in enumerate(HISTORY, 1):
                print(i, h)
            continue
        parts = line.split()
        cmd = parts[0].lower()
        if cmd == 'eval':
            expr = line[len('eval'):].strip()
            out = safe_eval(expr)
            print(out)
            continue
        if cmd == 'complex':
            if len(parts) >= 3:
                a = float(parts[1]); b = float(parts[2])
                print(complex(a, b))
            continue
        if cmd == 'frac':
            if len(parts) >= 3:
                print(Fraction(int(parts[1]), int(parts[2])))
            continue
        if cmd == 'quad':
            if len(parts) >= 4:
                print(solve_quadratic(parts[1], parts[2], parts[3]))
            continue
        if cmd == 'fact':
            if len(parts) >= 2:
                print(factorial(parts[1]))
            continue
        if cmd == 'perm':
            if len(parts) >= 3:
                print(nPr(parts[1], parts[2]))
            continue
        if cmd == 'comb':
            if len(parts) >= 3:
                print(nCr(parts[1], parts[2]))
            continue
        if cmd == 'baseconv':
            if len(parts) >= 4:
                print(base_convert(parts[1], parts[2], parts[3]))
            continue
        if cmd == 'bit':
            if len(parts) >= 4:
                print(bit_operation(parts[1], parts[2], parts[3]))
            continue
        if cmd == 'matrix':
            matrix_mode()
            continue
        if cmd == 'sym':
            expr = ' '.join(parts[1:])
            if not expr:
                continue
            var = 'x'
            toks = expr.split()
            if len(toks) >= 2 and toks[-1].isalpha() and len(toks[-1]) == 1:
                var = toks[-1]
                expr = ' '.join(toks[:-1])
            out = sym_mode(expr, var)
            print(out)
            continue
        res = safe_eval(line)
        print(res)

if __name__ == '__main__':
    repl()
