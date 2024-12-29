from point import Point
from ecc_operations import find_base_point, find_n, generate_curve, generate_keys, sign, verify, generate_prime

def app():
    print("Digital Signature App using ECC")
    # p = 907
    p = generate_prime(30)
    a, b = 1, 7
    # # # a, b = generate_curve(p)
    # p = 2701167613195130481826167156931545231582958730085772462601916414099154162919296538782370335616437698077798489651621592967846000281906070203543131
    G = find_base_point(a, b, p)

    # 30 bits => 182.19s find n
    # p = 987095027
    # a = 1
    # b = 7
    # G = Point(112870365, 782359001, (a, b, p))
    # n = 141018209

    # 256 bits secp256k1
    # p = int("0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f", 16)
    # a = 0
    # b = 7
    # G = Point(int("0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798", 16), int("0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8", 16), (a, b, p))
    # n = int("0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141", 16)

    # 521 bits secp521r1
    # p = int("0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)
    # a = int("0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc", 16)
    # b = int("0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00", 16)
    # G = Point(int("0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66", 16), 
    #           int("0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650", 16), (a, b, p))
    # n = int("0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409", 16)
    
    while True:
        print("\nOptions:")
        print("1. Generate Keys")
        print("2. Sign Message")
        print("3. Verify Signature")
        print("4. Exit")
        print("a = ", a)
        print("p = ", p)
        choice = input("Choose an option: ")
        if choice == '1':
            n = find_n(G)
            d, Q = generate_keys(G, n)
            print(f"Private Key (d): {d}")
            print(f"Public Key (Q): ({Q.x}, {Q.y})")
            print(f" (G): ({G.x}, {G.y})")
            print(f"n = {n}")
        elif choice == '2':
            m = input("Enter message to sign: ")
            r, s = sign(m, d, G, n)
            print(f"Signature: (r={r}, s={s})")
        elif choice == '3':
            m = input("Enter message to verify: ")
            r = int(input("Enter r: "))
            s = int(input("Enter s: "))
            result = verify(m, r, s, Q, G, n)
            print(f"Verification result: {'Valid' if result else 'Invalid'}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    app()