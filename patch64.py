import struct

# === KEY (64 bytes, extracted from the function constants) ===
def le64(v): return struct.pack('<Q', v)
def le32(v): return struct.pack('<I', v)

key = bytearray()
key += le32(0x3f8ff2d1)              # local_90 bytes 0-3
key += le32(0x0fc28bec)              # local_90 bytes 4-7
key += le64(0x8f79a608fcac2a38)      # uStack_88
key += le64(0x2fdf6a694db02512)      # pvStack_80
key += le64(0x0d9134c4510996b0)      # uStack_78
key += le64(0x1e800c011ceaf4b8)      # local_70
key += le64(0x40b8e8bc8e1bff20)      # uStack_68
key += le64(0xd15e1c13d22a15fb)      # uStack_60
key += le64(0xfbdf6f3184673222)      # uStack_58

# === Current encrypted BLOB (local_d0, 48 bytes) ===
cipher_actuel = bytearray([
    0xe4,0xc6,0xb7,0x5c,0x8e,0xbc,0xfa,0x36,  # bytes 0x00-0x07
    0x15,0x1a,0xca,0xc4,0x39,0x8b,0x4d,0xb6,  # bytes 0x08-0x0F
    0x26,0x11,0x9d,0x2c,0x5b,0x09,0xed,0x02,  # bytes 0x10-0x17
    0xd4,0xa3,0x68,0x60,0xa1,0x0d,0xa3,0x6e,  # bytes 0x18-0x1F
    0x81,0xc2,0xdf,0x79,0x01,0x73,0x80,0x1e,  # bytes 0x20-0x27
    0x97,0x20,0xf6,0xfe,0x43,0x97,0xb8,0x40,  # bytes 0x28-0x2F
])
cipher_actuel += bytearray(64 - len(cipher_actuel))  # 64-pad

# === VERIFICATION: Decrypt the old AppId ===
decrypte = bytearray(64)
for i in range(64):
    decrypte[i] = cipher_actuel[i] ^ key[i]
resultat = decrypte[:decrypte.index(b'\x00')].decode('ascii')
print("Decrypted  :", resultat)
print("Expected   : 548cb789-0f81-4944-a2c2-d5a1e92c965e")
print("Correct   :", resultat == "548cb789-0f81-4944-a2c2-d5a1e92c965e")

# === Configure your new Photon AppId ===
# Format WITH hyphens, ex : "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
nouvel_app_id = "2d868294-9ba2-4878-bf8f-66f883c4e96b"

plain = bytearray(nouvel_app_id.encode('ascii'))
plain += bytearray(64 - len(plain))  # pad with zeros

nouveau_blob = bytearray(64)
for i in range(64):
    nouveau_blob[i] = plain[i] ^ key[i]

print("\nNew encrypted blob (first 48 bytes to patch) :")
for i in range(0, 48, 8):
    print(' '.join(f'0x{b:02x}' for b in nouveau_blob[i:i+8]))

# === AUTOMATIC BINARY PATCHING ===
import re

with open("libMyGame64.so", "rb") as f:
    data = bytearray(f.read())

pattern = bytes(cipher_actuel[:36])  # Look for the first 36 bytes
pos = data.find(pattern)

if pos == -1:
    print("\nPATTERN NOT FOUND in the binary !")
else:
    print(f"\nFound at the offset 0x{pos:x}")
    # Replaces the 36 bytes of the AppId (the rest remains intact)
    data[pos:pos+36] = nouveau_blob[:36]
    with open("libMyGame64_patche.so", "wb") as f:
        f.write(data)
    print("Patched file saved : libMyGame64_patched.so")
