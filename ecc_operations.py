import random
import time
from point import Point
import gmpy2
import hashlib

def generate_prime(bits=480):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1
        if gmpy2.is_prime(p):
            return p

def generate_curve(p, max_attempts=1000, seed=None):
    if seed is not None:
        random.seed(seed)

    for attempt in range(max_attempts):
        a = random.randint(1, p - 1)
        b = random.randint(1, p - 1)
        if (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p != 0:
            return a, b
    
    raise ValueError(f"Unable to generate a valid curve after {max_attempts} attempts.")

def find_base_point(a, b, p):
    # This is a simplified version; in practice, finding the order is non-trivial.
    # For demonstration, we'll select a random point and assume it's a generator.
    while True:
        x = random.randint(0, p - 1)
        y_sq = (pow(x, 3, p) + a * x + b) % p
        try:
            y = pow(y_sq, (p + 1) // 4, p)
            if pow(y, 2, p) == y_sq:
                G = Point(x, y, (a, b, p))
                # Compute the order using Pollard's Rho algorithm (not implemented here)
                # For simplicity, assume the order is prime
                return G
        except ValueError:
            continue

def find_n(G):
    n = 1
    P = G
    start_time = time.time()
    last_print_time = start_time
    
    while P:
        if n % 1000000 == 0:
            current_time = time.time()
            elapsed_since_last = current_time - last_print_time
            total_elapsed = current_time - start_time
            print(f"n = {n}, nG = ({P.x}, {P.y}) ,Last: {elapsed_since_last:.2f} s, Sum: {total_elapsed:.2f} s")
            last_print_time = current_time 
        P += G
        n += 1
    return n

def generate_keys(G, n):
    d = random.randint(1, n - 1)
    Q = d * G
    return d, Q

def sign(m, d, G, n):
    H = int.from_bytes(hashlib.sha256(m.encode()).digest(), 'big')
    print(f"H = {H}")
    while True:
        k = random.randint(1, n - 1)
        try:
            k_inv = pow(k, -1, n)
        except ValueError:
            continue
        P = k * G
        r = P.x % n
        if r == 0:
            continue
        s = ((H + d * r) * k_inv) % n
        if s == 0:
            continue
        return (r, s)

def verify(m, r, s, Q, G, n):
    H = int.from_bytes(hashlib.sha256(m.encode()).digest(), 'big')
    print(f"H = {H}")
    if r < 1 or r >= n or s < 1 or s >= n:
        return False
    try:
        w = pow(s, -1, n)
    except ValueError:
        return False
    u1 = (H * w) % n
    u2 = (r * w) % n
    P = u1 * G + u2 * Q
    print(f"xxxxx = {P.x % n}")
    return P.x % n == r