# Modular Exponentiation
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Setup keys
p, q = 11, 13
n = p * q
e, d = 7, 103

# Message
m = 9
s = mod_exp(m, d, n)        # Sign
print("Signature:", s)

m_verify = mod_exp(s, e, n) # Verify
print("Verified Message:", m_verify)
print("Valid:", m_verify == m)



