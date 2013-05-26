import hashlib

def encrypt(plain, password):
    password = hashlib.md5(password).hexdigest()
    encrypted = []
    for x in plain:
        x = ord(x)
        for y in password:
           y = ord(y)
           x = x * y
        encrypted.append(str(x))
    
    return '/'.join(encrypted)



def decrypt(encrypted, password):
    data = encrypted.split("/")
    password = hashlib.md5(password).hexdigest()
    out = []
    for x in data:
        x = int(x)
        for y in password:
            y = ord(y)
            x = x/y
        out.append(chr(x))
    return ''.join(out)
