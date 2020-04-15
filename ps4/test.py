import string

print(string.ascii_lowercase)
print(string.ascii_uppercase)

shift = 26
print(shift)

shift = shift % 26
print(shift)
alphabet_lower = string.ascii_lowercase
alphabet_upper = string.ascii_uppercase
cipher_dict = {}
for i in range(len(alphabet_lower)):
    cipher_dict[alphabet_lower[i]] = alphabet_lower[shift-len(alphabet_lower) + i]
for i in range(len(alphabet_upper)):
    cipher_dict[alphabet_upper[i]] = alphabet_upper[shift-len(alphabet_upper) + i]

print(cipher_dict)
print(len(alphabet_lower))
