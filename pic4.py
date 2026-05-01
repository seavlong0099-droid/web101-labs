# Modular Exponentiation Algorithm
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# 1. Setup Keys (p=11, q=13)
n = 143  # p * q
e, d = 7, 103  # Public, Private

# 2. Sign Message (m=9)
message = 9
signature = mod_exp(message, d, n)
print("Signature:", signature)

# 3. Verify Signature
verified = mod_exp(signature, e, n)
print("Verified Message:", verified)

# Check validity
is_valid = (message == verified)
print("Valid:", is_valid)