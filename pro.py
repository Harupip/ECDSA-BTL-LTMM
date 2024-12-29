# cypher = input("Input cypher text: ")
# text = input("Input plain text: ")
# shift_num = int(input("Number of shifts: "))
# key = input("Input key text: ")
# a = int(input("a: "))
# b = int(input("b: "))

def multi_input():
  cont = 1
  while (cont):
    text = input("Input plain text: ")
    print(find_letter_code(text))
    # cont = int(input("Continue? (1/0): "))
  
def find_letter_code(letter):
  return ord(letter.upper()) - 65

def decrypt(cypher):
  for i in range(0, 26):
    print(i, end=": ")
    decrypted_text = ""
    for j in range(0, len(cypher)):
      if cypher[j] == " ":
        decrypted_text += " "
        print(" ", end="")
      else:
        shift = ord(cypher[j]) - i
        if shift < ord("A"):
          shift = shift + 26
        decrypted_text += chr(shift)
        # print(chr(shift), end="")
    print(decrypted_text, end="")
    print("\n")


def encrypt(text, shift_num):
  if shift_num > 25:
    shift_num = shift_num % 26

  encrypted_text = ""
  for j in range(0, len(text)):
    if text[j] == " ":
      encrypted_text += " "
      # print(" ", end="")
    else:
      shift = ord(text[j]) + shift_num
      if shift > ord("Z"):
        shift = shift - 26
      encrypted_text += chr(shift)
      # print(chr(shift), end="")
  return encrypted_text

def vigenere_encrypt(text, key):
  encrypted_text = ""
  key_count = len(key)
  count = 0
  for char in text.upper():
      if char == " ":
          encrypted_text += " "
      elif char.isalpha():
          shift = (ord(char) - 65 + ord(key[count % key_count].upper()) - 65) % 26
          encrypted_text += chr(shift + 65)
          count += 1
      else:
          encrypted_text += char
  return encrypted_text

def vigenere_decrypt(text, key):
  decrypted_text = ""
  key_count = len(key)
  count = 0
  for char in text.upper():
      if char == " ":
          decrypted_text += " "
      elif char.isalpha():
          shift = (ord(char) - 65 - ord(key[count % key_count].upper()) - 65) % 26
          decrypted_text += chr(shift + 65)
          count += 1
      else:
          decrypted_text += char
  return decrypted_text

def modular_inverse(b, m):
  def extended_euclid(a, b):
      # Hàm Euclid mở rộng
      if b == 0:
          return a, 1, 0  # GCD(a, b), x, y
      gcd, x1, y1 = extended_euclid(b, a % b)
      x = y1
      y = x1 - (a // b) * y1
      return gcd, x, y

  gcd, x, _ = extended_euclid(b, m)
  if gcd != 1:
      raise ValueError(f"Nghịch đảo không tồn tại vì GCD({b}, {m}) != 1.")
  return x % m  # Đảm bảo x là số dương

def modular_inverse2(a, m):
  xa, xm = 1, 0
  while m != 0:
      q = a // m
      xr = xa - q * xm
      xa, xm = xm, xr
      r = a % m
      a, m = m, r
  return xa

def euclid_extended(a, m):
  y0, y1 = 0, 1
  print("  n     " + "     m     " + "     r     " + "q " + "        y0    " + "    y1    "+"    y    ")
  while a > 0:
      r = m % a
      if r == 0:
          break
      q = m // a
      y = y0 - y1 * q
      y0, y1 = y1, y
      m, a = a, r
      print(f"{str(a):<10}{str(m):<10}{str(r):<10}{str(q):<10}{str(y0):<10}{str(y1):<10}{str(y):<10}")
  if a > 1:
      return "A không khả nghịch theo modulo m"
  else:
      return f"Nghịch đảo modulo {m} của a "
      
def eliptic(num):
    n = []
    for i in range(1, num):
        n.append(i**2 % num)
        print(f"{i} = {i**2 % num}")
    return list(set(n))

def find_point(a, b, num):
    check = eliptic(num)
    n = []
    for x in range(0, num):
      m = x**3 + a * x + b
      m = m % num
      print(f"{x} = {m}")
      if m in check:
          n.append(x)
    print(f"len = {len(n) * 2 + 1}")
    print(f"middle = {n[len(n) // 2]}")
    return n

def subtract_largest_power_of_two(n):
    a = 0
    while (1 << a) <= n:
        a += 1
    a -= 1

    largest_power_of_two = 1 << a
    result = n - largest_power_of_two
    return result, a

def cal_lamda_elpitic(x1, y1, x2, y2, a, mod):
    if (x1 == x2 and y1 == y2):
        tu = 3 * x1**2 + a
        mau = 2 * y1
        if (mau == 0):
            print("tiem can")
            return 0
        elif (tu % mau == 0):
            return (tu/mau) % mod
        else:
            mau = modular_inverse(mau, mod)
            print(f"x = {mau} , {(tu * mau) % mod}")
            return (tu * mau) % mod
    else:
        tu = y2 - y1
        mau = x2 - x1
        if (mau == 0):
            print("tiem can")
            return 0
        elif (tu % mau == 0):
            return (tu/mau) % mod
        else:
            mau = modular_inverse(mau, mod)
            return (tu * mau) % mod

def cal_x3_y3(a, mod, x1, y1, x2, y2, p):
    if (p < 2):
        print("p khong hop le")
        return 0
    lamda = cal_lamda_elpitic(x1, y1, x2, y2, a, mod)
    print(lamda)
    x3 = (lamda**2 - x1 - x2) % mod
    y3 = (lamda * (x1 - x3) - y1) % mod
    if (p == 2):
        # print(f"{p} = ({x3}, {y3})")
        return x3, y3
    else:
        l1, l2 = subtract_largest_power_of_two(p)
            
        for i in range (0, l2 - 1):
            lamda = cal_lamda_elpitic(x3, y3, x3, y3, a, mod)
            x = x3
            x3 = (lamda**2 - x3 - x3) % mod
            y3 = (lamda * (x - x3) - y3) % mod

        for i in range (0, l1):
            lamda = cal_lamda_elpitic(x3, y3, x1, y1, a, mod)
            x = x3
            x3 = (lamda**2 - x1 - x3) % mod
            y3 = (lamda * (x1 - x3) - y1) % mod

        return x3, y3

def cal_x3_y3_no_p(a, mod, x1, y1):
    lamda = cal_lamda_elpitic(x1, y1, x1, y1, a, mod)
    x3 = (lamda**2 - x1 - x1) % mod
    y3 = (lamda * (x1 - x3) - y1) % mod
    print(f"2 : ({x3}, {y3})")
    count = 2
    while (x1 != x3):
        count += 1
        lamda = cal_lamda_elpitic(x3, y3, x1, y1, a, mod)
        # x = x3
        x3 = (lamda**2 - x1 - x3) % mod
        y3 = (lamda * (x1 - x3) - y1) % mod
        print(f"{count} : ({x3}, {y3})")
    print(count + 1)
    return x3, y3
    
# print(decrypt(cypher))
# print(encrypt(text, shift_num))
# print(find_letter_code(text))
# print(vigenere_encrypt(text, key))
# print(vigenere_decrypt(text, key))

# multi_input()
# print(modular_inverse(a, b))
# print(modular_inverse2(a, b))
#print(euclid_extended(a, b))
# print(eliptic(b))
# print(find_point(3, 2, 41))
#print(cal_x3_y3(4, 37, 20, 24, 32, 26, 2))
print(cal_x3_y3_no_p(1, 907, 500, 88))

