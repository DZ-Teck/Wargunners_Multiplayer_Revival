# Key (identical for 32-bit and 64-bit)
key = bytes([
    0xd1,0xf2,0x8f,0x3f,0xec,0x8b,0xc2,0x0f,
    0x38,0x2a,0xac,0xfc,0x08,0xa6,0x79,0x8f,
    0x12,0x25,0xb0,0x4d,0x69,0x6a,0xdf,0x2f,
    0xb0,0x96,0x09,0x51,0xc4,0x34,0x91,0x0d,
    0xb8,0xf4,0xea,0x1c,0x01,0x0c,0x80,0x1e,
    0x20,0xff,0x1b,0x8e,0xbc,0xe8,0xb8,0x40,
    0xfb,0x15,0x2a,0xd2,0x13,0x1c,0x5e,0xd1,
    0x22,0x32,0x67,0x84,0x31,0x6f,0xdf,0xfb,
])

# === Configure your new Photon AppId ===
# Format WITH hyphens, ex : "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
old_appid = "548cb789-0f81-4944-a2c2-d5a1e92c965e"
new_appid  = "2d868294-9ba2-4878-bf8f-66f883c4e96b"

def chiffrer(appid, key):
    plain = appid.encode('ascii') + b'\x00'
    plain = plain.ljust(64, b'\x00')
    return bytes(p ^ k for p, k in zip(plain, key))

new_cipher = chiffrer(new_appid, key)

with open("libMyGame32.so", "rb") as f:
    data = bytearray(f.read())

# Look for the key in the binary
key_pos = data.find(key)
if key_pos == -1:
    print("ERROR: key not found in the binary!")
    exit()

print(f"Key found at the offset: 0x{key_pos:x}")

# The cipher blob is exactly 0x40 bytes after the key
# (0x7fbda8 - 0x7fbd68 = 0x40)
cipher_pos = key_pos + 0x40
cipher_actuel = bytes(data[cipher_pos:cipher_pos+64])

# Vérification
dec = bytes(c ^ k for c, k in zip(cipher_actuel, key))
dec_str = dec[:dec.index(b'\x00')].decode('ascii')
print(f"AppId decrypted : {dec_str}")
print(f"Expected         : {old_appid}")
print(f"Correct         : {dec_str == old_appid}")

if dec_str != old_appid:
    print("ERROR: verification failed, not patching.")
    exit()

# Patch
data[cipher_pos:cipher_pos+64] = new_cipher
with open("libMyGame32_patched.so", "wb") as f:
    f.write(data)

print(f"\nPatched file saved : libMyGame32_patched.so")
