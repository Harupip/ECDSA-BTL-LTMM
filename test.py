from ecdsa import SECP256k1

# Lấy điểm G từ SECP256k1
G = SECP256k1.generator

# Tọa độ của điểm G (x, y)
Gx = G.x()
Gy = G.y()
p = G.curve().p()

# In ra tọa độ x, y của điểm G
print(f"Point G coordinates: x = {hex(Gx)}, y = {hex(Gy)}")
print(f"Point G coordinates: x = {Gx}, y = {Gy}, p = {hex(p)}")
print(pow(10, -1, 17))