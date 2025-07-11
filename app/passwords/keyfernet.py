#from cryptography.fernet import Fernet
#print(Fernet.generate_key().decode())

#from werkzeug.security import generate_password_hash
#print(generate_password_hash("admin"))


#from werkzeug.security import generate_password_hash

# Cambia "admin" por la contraseña que uses
#print(generate_password_hash("admin"))

#from werkzeug.security import generate_password_hash

#print(generate_password_hash("admin"))

#print(generate_password_hash("abcd"))
from passlib.hash import scrypt

hash = scrypt.hash("P3dr0G@l1nd0")  # o cualquier contraseña
print(hash)