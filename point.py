class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve  # (a, b, p)
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y) if other else False
    
    def __bool__(self):
        return self.x is not None and self.y is not None
    
    def __neg__(self):
        return Point(self.x, -self.y % self.curve[2], self.curve)
    
    def __add__(self, other):
        if not self or not other:
            return self if other else other
        a, b, p = self.curve
        if self.x == other.x and self.y != other.y:
            return Point(None, None, self.curve)
        if self.x == other.x:
            m = ((3 * pow(self.x, 2) + a) * pow(2 * self.y, -1, p)) % p
        else:
            m = ((other.y - self.y) * pow(other.x - self.x, -1, p)) % p
        x3 = (m * m - self.x - other.x) % p
        y3 = (m * (self.x - x3) - self.y) % p
        return Point(x3, y3, self.curve)
    
    def __rmul__(self, k):
        Q = Point(self.x, self.y, self.curve)
        k_bin = bin(k)[2:]
        for bit in k_bin[1:]:
            Q += Q
            if bit == '1':
                Q += self
        return Q
    
